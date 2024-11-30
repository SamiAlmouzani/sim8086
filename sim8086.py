import sys, io

field_encW0 = {'000': 'al', '001': 'cl', '010': 'dl', '011': 'bl', '100': 'ah', '101': 'ch', '110': 'dh', '111': 'bh'}
field_encW1 = {'000': 'ax', '001': 'cx', '010': 'dx', '011': 'bx', '100': 'sp', '101': 'bp', '110': 'si', '111': 'di'}
eff_addr_calc = {'000': 'bx + si', '001': 'bx + di', '010': 'bp + si', '011': 'bp + di', '100': 'si', '101': 'di', '110': 'bp', '111': 'bx'}

def read_binary(file_path: str):
    with open(file_path, 'rb') as file:
        # print(f"{type(file)}: {str(file.read())}")
        return file.read()

# 1011 w reg  data  data if w=1
def immediate_to_reg(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    # 10110001
    # print(f'b1: {b1}')
    wide = b1[4]
    reg = b1[5:]
    data = None
    # if wide == '0':
    #     data = f'{b_list.pop(0):08b}'
    # else:
    #     data = f'{b_list.pop(0):08b}{b_list.pop(0):08b}'
    data = f'{b_list.pop(0):08b}' if wide == '0' else  f'{b_list.pop(1):08b}{b_list.pop(0):08b}'
    # print(f'data: {data}')
    reg = field_encW0[reg] if wide == '0' else field_encW1[reg] 
    return 'mov', reg, int(data, 2)

def regmem_to_regmem(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    dest = b1[6]
    wide = b1[7]
    b2: str = f'{b_list.pop(0):08b}'
    mod = b2[:2]
    reg = b2[2:5]
    rm = b2[5:]
    # print(f"# op_code: {b1[:6]}   dest: {dest}   wide: {wide}   mod: {mod}   reg: {reg}    rm: {rm}")

    # find register value field encoding
    reg = field_encW0[reg] if wide == '0' else field_encW1[reg] 
    if mod == '11':
        rm = field_encW0[rm] if wide == '0' else field_encW1[rm]    
        pass
    if mod == '00':
        rm = f'[{eff_addr_calc[rm]}]' if rm != '110' else f'{b_list.pop(1):08b}{b_list.pop(0):08b}'
    if mod == '01':
        dp = b_list.pop(0)
        rm = f'[{eff_addr_calc[rm]} + {dp}]' if dp else f'[{eff_addr_calc[rm]}]' 
    if mod == '10':
        dp = f'{b_list.pop(1):08b}{b_list.pop(0):08b}'
        dp_int = int(dp, 2)
        rm = f'[{eff_addr_calc[rm]} + {dp_int}]' if dp_int else f'[{eff_addr_calc[rm]}]' 

    # checks the D (dest) bit to see which is dest and src
    dest, src = (reg, rm) if dest == '1' else (rm, reg)
    
    return 'mov', dest, src

def get_disassembly(b_list: list[int]) -> tuple[str, str, str]:
    # converts to binary and removes '0b' prefix
    b1: str = f'{b_list.pop(0):08b}'
    if b1[:4] == '1011':
        return immediate_to_reg(b1, b_list)
    if b1[:6] == '100010':
        return regmem_to_regmem(b1, b_list)
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
    # for i in range(len(bytes)):
    #     if i % 2 == 0:
    #         continue
    #     instr, dest, src = get_disassembly(view[i-1], view[i])
    #     print(f"{instr} {dest}, {src}")



        