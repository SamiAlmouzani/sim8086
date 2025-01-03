import sys, io, argparse

field_encW0 = {'000': 'al', '001': 'cl', '010': 'dl', '011': 'bl', '100': 'ah', '101': 'ch', '110': 'dh', '111': 'bh'}
field_encW1 = {'000': 'ax', '001': 'cx', '010': 'dx', '011': 'bx', '100': 'sp', '101': 'bp', '110': 'si', '111': 'di'}
eff_addr_calc = {'000': 'bx + si', '001': 'bx + di', '010': 'bp + si', '011': 'bp + di', '100': 'si', '101': 'di', '110': 'bp', '111': 'bx'}
op_type = {'000': 'add', '101': 'sub', '111': 'cmp'}

regs: dict[str, int] = {'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0, 'sp': 0, 'bp': 0, 'si': 0, 'di': 0}
z_flag: int = 0
s_flag: int = 0

def read_binary(file_path: str):
    with open(file_path, 'rb') as file:
        return file.read()

def mode_enc(mod: str, rm: str, wide: str, b_list: list[int]) -> str:
    # use correct mode field encoding
    if mod == '11':
        rm = field_encW0[rm] if wide == '0' else field_encW1[rm]    
    if mod == '00':
        if rm != '110': rm = f'[{eff_addr_calc[rm]}]'
        else:
            bit_str: str = f'{b_list.pop(1):08b}{b_list.pop(0):08b}'
            num: int = int(bit_str, 2)
            rm: str = f'[{num}]'
    if mod == '01':
        dp = b_list.pop(0)
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
    # if mod == '01': print(f"; op_code: {b1[:6]}   dest: {dest}   wide: {wide}   mod: {mod}   reg: {reg}    rm: {rm}")
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
    rm = mode_enc(mod, rm, wide, b_list)
    data: str = f'{b_list.pop(1):08b}{b_list.pop(0):08b}' if signed == '0' and wide == '1'  else f'{b_list.pop(0):08b}'
    if mod != '11':
        rm: str = f'byte {rm}' if wide == '0' else f'word {rm}'
    return op, rm, int(data, 2)

def imm_to_acc(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    op: str = op_type[b1[2:5]]
    wide: str = b1[7]
    reg, data = ('ax', f'{b_list.pop(1):08b}{b_list.pop(0):08b}') if wide == '1' else ('al', f'{b_list.pop(0):08b}') 
    return op, reg, int(data, 2)

def get_disassembly(b1: str, b_list: list[int], args) -> str:
    global z_flag
    global s_flag 
    if b1[:4] == '1011': # mov reg, 5
        instr, dest, src = immediate_to_reg(b1, b_list)
        line: str = f'{instr} {dest}, {src} ; {dest}:{hex(regs[dest])}->{hex(src)}' if args.exec else f'{instr} {dest}, {src}'
        regs[dest] = src
        return line 
    if b1[:6] == '100010': # mov reg, rm
        instr, dest, src = mov_rm_to_rm(b1, b_list)
        line: str = f'{instr} {dest}, {src} ; {dest}:{hex(regs[dest])}->{hex(regs[src])}' if args.exec else f'{instr} {dest}, {src}'
        regs[dest] = regs[src]
        return line
    if b1[:2] == '00' and b1[5] == '0': # arithmetic with register/memory
        instr, dest, src =  arith_with_rm(b1, b_list)
        result: int 
        if args.exec:
            if instr == 'add': 
                result = int(regs[dest]) + int(regs[src])
            if instr == 'sub': 
                result = int(regs[dest]) - int(regs[src]) 
            if instr == 'cmp': 
                result = int(regs[dest]) - int(regs[src])
        # set flags
        prev_z_flag: str = '' if z_flag == 0 else 'Z'
        prev_s_flag: str = '' if s_flag == 0 else 'S'
        z_flag = 1 if result == 0 else 0
        # checks if most significant bit is 1 or 0
        bin_result: str = f'{result:016b}'
        print(f'bin_result: {bin_result}')
        s_flag = int(bin_result[0])
        curr_z_flag: str = '' if z_flag == 0 else 'Z'
        curr_s_flag: str = '' if s_flag == 0 else 'S'
        asm_line: str = f'{instr} {dest}, {src} ; ' 
        if instr != 'cmp':
            reg_info: str = f'{dest}:{hex(regs[dest])}->{hex(result)} flags:{prev_s_flag}{prev_z_flag}->{curr_s_flag}{curr_z_flag}' if args.exec else f'{instr} {dest}, {src}'
            # update dest register with new value
            regs[dest] = result
        else:
            reg_info: str = f'flags:{prev_s_flag}{prev_z_flag}->{curr_s_flag}{curr_z_flag}' if args.exec else f'{instr} {dest}, {src}'
        return asm_line + reg_info

    if b1[:6] == '100000': # arithmetic with immediate
        instr, dest, src = arith_with_imm(b1, b_list)
        result: int 
        if args.exec:
            if instr == 'add': 
                result = int(regs[dest]) + int(src)
            if instr == 'sub': 
                result = int(regs[dest]) - int(src) 
            if instr == 'cmp': 
                result = int(regs[dest]) - int(src)
        # set flags
        prev_z_flag: str = '' if z_flag == 0 else 'Z'
        prev_s_flag: str = '' if s_flag == 0 else 'S'
        z_flag = 1 if result == 0 else 0
        # checks if most significant bit is 1 or 0
        bin_result: str = f'{result:016b}'
        print(f'bin_result: {bin_result}')
        s_flag = int(bin_result[0])
        curr_z_flag: str = '' if z_flag == 0 else 'Z'
        curr_s_flag: str = '' if s_flag == 0 else 'S'
        asm_line: str = f'{instr} {dest}, {src} ; ' 
        if instr != 'cmp':
            reg_info: str = f'{dest}:{hex(regs[dest])}->{hex(result)} flags:{prev_s_flag}{prev_z_flag}->{curr_s_flag}{curr_z_flag}' if args.exec else f'{instr} {dest}, {src}'
            # update dest register with new value
            regs[dest] = result
        else:
            reg_info: str = f'flags:{prev_s_flag}{prev_z_flag}->{curr_s_flag}{curr_z_flag}' if args.exec else f'{instr} {dest}, {src}'
        return asm_line + reg_info

    if b1[:2] == '00' and b1[5:7] == '10':
        instr, dest, src = imm_to_acc(b1, b_list)
        return f'{instr} {dest}, {src}'
    if b1 == '01110101': # jump if not equal to zero
        return f'jnz ; {b_list.pop(0)}'
    if b1 == '01110100': # jump on equal zero
        return f'je ; {b_list.pop(0)}'
    if b1 == '01111100': # jump on less
        return f'jl ; {b_list.pop(0)}'
    if b1 == '01111110': # jump on less/equal
        return f'jle ; {b_list.pop(0)}'
    if b1 == '01110010': # jump on below/not above or equal
        return f'jb ; {b_list.pop(0)}'
    if b1 == '01110110': # jump on below/equal not above
        return f'jbe ; {b_list.pop(0)}'
    if b1 == '01111010': # jump on parity/parity even
        return f'jp ; {b_list.pop(0)}'
    if b1 == '01110000': # jump on overflow 
        return f'jo ; {b_list.pop(0)}'
    if b1 == '01111000': # jump on sign
        return f'js ; {b_list.pop(0)}'
    if b1 == '01111101': # jump on not less/greater or equal
        return f'jnl ; {b_list.pop(0)}'
    if b1 == '01111111': # jump on not less or equal/greater
        return f'jg ; {b_list.pop(0)}'
    if b1 == '01110011': # jump on not below/above or equal
        return f'jnb ; {b_list.pop(0)}'
    if b1 == '01110111': # jump on not below/above or equal
        return f'ja ; {b_list.pop(0)}'
    if b1 == '01111011': # jump on not par/par odd
        return f'jnp ; {b_list.pop(0)}'
    if b1 == '01110001': # jump on not overflow
        return f'jno ; {b_list.pop(0)}'
    if b1 == '01111001': # jump on not sign
        return f'jns ; {b_list.pop(0)}'
    if b1 == '11100010': # loop cx times 
        return f'loop ; {b_list.pop(0)}'
    if b1 == '11100001': # loop while zero/equal
        return f'loopz ; {b_list.pop(0)}'
    if b1 == '11100000': # loop while not zero/equal
        return f'loopnz ; {b_list.pop(0)}'
    if b1 == '11100011': # loop while not zero/equal
        return f'jcxz ; {b_list.pop(0)}'
    raise ValueError(f'Wrong assembly instruction! instr: {b1}')
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-exec', action='store_true')
    parser.add_argument('filename')
    args = parser.parse_args()

    print(f"; {args.filename}")
    print(f'bits 16\n')
    bytes = read_binary(args.filename)
    b = io.BytesIO(bytes)
    b_list = b.getbuffer().tolist()
    while b_list:
        # converts to binary and removes '0b' prefix
        b1: str = f'{b_list.pop(0):08b}'
        line: str = get_disassembly(b1, b_list, args)
        # print(f'current flags: {s_flag}{z_flag}')
        print(line)  
    if args.exec:
        print(f'\nFinal Registers:')
        for k, v in regs.items():
            print(f'\t{k}: {hex(v)} ({v})')
        print(f"  flags:{s_flag or ''}{z_flag or ''}")


        