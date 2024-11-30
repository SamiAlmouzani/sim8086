import sys, io

field_encW0 = {'000': 'al', '001': 'cl', '010': 'dl', '011': 'bl', '100': 'ah', '101': 'ch', '110': 'dh', '111': 'bh'}
field_encW1 = {'000': 'ax', '001': 'cx', '010': 'dx', '011': 'bx', '100': 'sp', '101': 'bp', '110': 'si', '111': 'di'}
eff_addr_calc = {'000': 'bx + si', '001': 'bx + di', '010': 'bp + si', '011': 'bp + di', '100': 'si', '101': 'di', '110': 'bp', '111': 'bx'}
op_type = {'000': 'add', '101': 'sub', '111': 'cmp'}

def read_binary(file_path: str):
    with open(file_path, 'rb') as file:
        return file.read()

def mode_enc(mod: str, rm: str, wide: str, b_list: list[int]) -> str:
    # use correct mode field encoding
    if mod == '11':
        rm = field_encW0[rm] if wide == '0' else field_encW1[rm]    
        pass
    if mod == '00':
        rm = f'[{eff_addr_calc[rm]}]' if rm != '110' else f'{b_list.pop(1):08b}{b_list.pop(0):08b}'
    if mod == '01':
        dp = b_list.pop(0)
        # rm = f'[{eff_addr_calc[rm]} + {dp}]' if dp else f'[{eff_addr_calc[rm]}]' 
        rm = f'[{eff_addr_calc[rm]} + {dp}]' 
    if mod == '10':
        dp = f'{b_list.pop(1):08b}{b_list.pop(0):08b}'
        dp_int = int(dp, 2)
        rm = f'[{eff_addr_calc[rm]} + {dp_int}]' if dp_int else f'[{eff_addr_calc[rm]}]' 
    return rm

# 1011 w reg | data  data if w=1
def immediate_to_reg(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    wide = b1[4]
    reg = b1[5:]
    data = f'{b_list.pop(0):08b}' if wide == '0' else  f'{b_list.pop(1):08b}{b_list.pop(0):08b}'
    reg = field_encW0[reg] if wide == '0' else field_encW1[reg] 
    return 'mov', reg, int(data, 2)

# 100010 d w | mod reg rm
def mov_rm_to_rm(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    dest = b1[6]
    wide = b1[7]
    b2: str = f'{b_list.pop(0):08b}'
    mod = b2[:2]
    reg = b2[2:5]
    rm = b2[5:]
    # print(f"# op_code: {b1[:6]}   dest: {dest}   wide: {wide}   mod: {mod}   reg: {reg}    rm: {rm}")
    # find register value field encoding
    reg = field_encW0[reg] if wide == '0' else field_encW1[reg] 
    rm = mode_enc(mod, rm, wide, b_list)
    # checks the D (dest) bit to see which is dest and src
    dest, src = (reg, rm) if dest == '1' else (rm, reg)
    return 'mov', dest, src

def arith_with_rm(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    op:str = op_type[b1[2:5]]
    _, dest, src = mov_rm_to_rm(b1, b_list)
    return op, dest, src

def arith_with_imm(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    signed: str = b1[6]
    wide: str = b1[7]
    b2: str = f'{b_list.pop(0):08b}'
    mod: str = b2[:2]
    op: str = op_type[b2[2:5]]
    rm: str = b2[5:] 

    # print(f'b1: {b1} and b2: {b2} and b3: {b_list.pop(0):08b}')
    # exit()
    # print(f"; op_code: {b1[:6]}   signed: {signed}   wide: {wide}   mod: {mod}   op: {op}  rm: {rm}")
    rm = mode_enc(mod, rm, wide, b_list)
    data: str = f'{b_list.pop(1):08b}{b_list.pop(0):08b}' if signed == '0' and wide == '1'  else f'{b_list.pop(0):08b}'
    if mod != '11':
        rm: str = f'byte {rm}' if wide == '0' else f'word {rm}'
    # print(f'; data: {data}')
    return op, rm, int(data, 2)

def imm_to_acc(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    wide: str = b1[7]
    reg, data = ('ax', f'{b_list.pop(1):08b}{b_list.pop(0):08b}') if wide == '1' else ('al', f'{b_list.pop(0):08b}') 
    return 'add', reg, int(data, 2)


def get_disassembly(b_list: list[int]) -> tuple[str, str, str]:
    # converts to binary and removes '0b' prefix
    b1: str = f'{b_list.pop(0):08b}'
    if b1[:4] == '1011': # mov reg, 5
        return immediate_to_reg(b1, b_list)
    if b1[:6] == '100010': # mov reg, rm
        return mov_rm_to_rm(b1, b_list)
    if b1[:6] == '000000': # arithmetic with register/memory
        return arith_with_rm(b1, b_list)
    if b1[:6] == '100000': # arithmetic with immediate
        return arith_with_imm(b1, b_list)
    if b1[:7] == '0000010':
        return imm_to_acc(b1, b_list)
    raise ValueError(f'Wrong assembly instruction! instr: {b1}')

if __name__ == "__main__":
    print(f"; {sys.argv[1]}")
    print(f'bits 16\n')
    bytes = read_binary(sys.argv[1])
    b = io.BytesIO(bytes)
    b_list = b.getbuffer().tolist()
    while b_list:
        instr, dest, src = get_disassembly(b_list)
        print(f"{instr} {dest}, {src}")



        