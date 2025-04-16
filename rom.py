
def pad_with_zeroes(array: list, final_length = 2**8, padding = "0"*16):
    while len(array) < final_length:
        array.append(padding)
    
    return array

def add_line_separators(array: list):
    for index, value in enumerate(array):
        array[index] = value + "\n"

    return array

def output_rom(instructions: list, filename):
    
    if len(instructions) > (2**8):
        instructions_a = instructions[:2**8]
        instructions_b = pad_with_zeroes(instructions[2**8:])
    else:
        instructions_a = pad_with_zeroes(instructions)
        instructions_b = pad_with_zeroes([])
    
    with open(filename + "_a.bin", "w") as f:
        instructions_a = add_line_separators(instructions_a)
        f.writelines(instructions_a)
    
    with open(filename + "_b.bin", "w") as f:
        instructions_b = add_line_separators(instructions_b)
        f.writelines(instructions_b)

    return instructions_a, instructions_b

if __name__ == "__main__":
    output_rom(["0"*16, "1"*16, "0"*8 + "1"*8], "test")