import sys, io

field_encW0 = {'000': 'al', '001': 'cl', '010': 'dl', '011': 'bl', '100': 'ah', '101': 'ch', '110': 'dh', '111': 'bh'}
field_encW1 = {'000': 'ax', '001': 'cx', '010': 'dx', '011': 'bx', '100': 'sp', '101': 'bp', '110': 'si', '111': 'di'}

def read_binary(file_path: str):
    with open(file_path, 'rb') as file:
        # print(f"{type(file)}: {str(file.read())}")
        return file.read()

def dissasemble(v1, v2):
    # converts to binary and removes '0b' prefix
    bin1: str = bin(v1)[2:]
    bin2: str = bin(v2)[2:]
    op_code = bin1[:6]

    instruction = None
    if op_code == "100010":
        instruction = "mov"
    dest = bin1[6]
    wide = bin1[7]

    mod = bin2[:2]
    reg = bin2[2:5]
    rm = bin2[5:]
    # print(f"# op_code: {op_code}   dest: {dest}   wide: {wide}   mod: {mod}   reg: {reg}    rm: {rm}")
    #TODO mod is not used yet, right now it is between reg to reg
    reg, rm = (field_encW0[reg], field_encW0[rm]) if wide == '0' else (field_encW1[reg], field_encW1[rm]) 
    
    # checks the D (dest) bit to see which is dest and src
    dest, src = (reg, rm) if dest == '1' else (rm, reg)
    
    return instruction, dest, src

if __name__ == "__main__":
    print(f"; {sys.argv[1]}")
    print(f'bits 16')
    bytes = read_binary(sys.argv[1])
    b = io.BytesIO(bytes)
    view = b.getbuffer()
    for i in range(len(bytes)):
        if i % 2 == 0:
            continue
        instr, dest, src = dissasemble(view[i-1], view[i])
        print(f"{instr} {dest}, {src}")



        