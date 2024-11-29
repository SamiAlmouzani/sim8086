import sys, io

field_encW0 = {'000': 'al', '001': 'cl', '010': 'dl', '011': 'bl', '100': 'ah', '101': 'ch', '110': 'dh', '111': 'bh'}
field_encW1 = {'000': 'ax', '001': 'cx', '010': 'dx', '011': 'bx', '100': 'sp', '101': 'bp', '110': 'si', '111': 'di'}

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
    data = f'{b_list.pop(0):08b}' if wide == '0' else  f'{b_list.pop(0):08b}{b_list.pop(0):08b}'
    # print(f'data: {data}')
    reg= field_encW0[reg] if wide == '0' else field_encW1[reg] 
    return 'mov', reg, int(data, 2)

def regmem_to_regmem(b1: str, b_list: list[int]) -> tuple[str, str, str]:
    dest = b1[6]
    wide = b1[7]
    b2: str = bin(b_list.pop(0))[2:]
    mod = b2[:2]
    reg = b2[2:5]
    rm = b2[5:]
    # print(f"# op_code: {op_code}   dest: {dest}   wide: {wide}   mod: {mod}   reg: {reg}    rm: {rm}")
    #TODO mod is not used yet, right now it is between reg to reg
    reg, rm = (field_encW0[reg], field_encW0[rm]) if wide == '0' else (field_encW1[reg], field_encW1[rm]) 
    
    # checks the D (dest) bit to see which is dest and src
    dest, src = (reg, rm) if dest == '1' else (rm, reg)
    
    return 'mov', dest, src

def get_disassembly(b_list: list[int]) -> tuple[str, str, str]:
    # converts to binary and removes '0b' prefix
    b1: str = bin(b_list.pop(0))[2:]
    if b1[:4] == '1011':
        return immediate_to_reg(b1, b_list)
    if b1[:6] == '100010':
        return regmem_to_regmem(b1, b_list)
    raise ValueError("Wrong assembly instruction!")

if __name__ == "__main__":
    print(f"; {sys.argv[1]}")
    print(f'bits 16')
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



        