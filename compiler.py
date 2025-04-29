import datetime
import json
import sys
import time
import os

import rom
import validator

assert len(sys.argv) > 1, "Target expected - example command: python compiler.py example.asm"

with open("commands.json") as f: COMMANDS : dict = json.load(f)
with open("keywords.json") as f: KEYWORDS : dict = json.load(f)

for i in COMMANDS.keys():
    KEYWORDS[i] = COMMANDS.get(i)

del COMMANDS

TARGET = sys.argv[1]
FORCE_BUILD = "--force" in sys.argv

assert os.path.exists(os.path.abspath(TARGET)), f"The file {os.path.abspath(TARGET)} ({TARGET}) doesn't exist or could not be accessed."

PADDING = {
    " ": 8,
    "r": 4,
    "l": 9
}

def convert_binary(number : int, padding = 4):
    default_conversion = bin(number)[2:]

    if padding is None:
        padding = 0
    
    return "0" * (padding - len(default_conversion)) + default_conversion

def compile_file(program : str):
    lines = program.split("\n")

    machine_code_lines = []

    print("Compiling...", end="")
    for line in lines:
        if len(line.strip()) < 2 or line[0] == "#":
            continue

        new_line = ""
        number = ""
        last_char = ""
        for i in line+" ":
            if i == "#":
                break

            if not i.isdigit():
                if number != "":
                    padding = PADDING.get(last_char)
                    if last_char == "l":
                        number = str(int(number) - 1)

                    new_line += convert_binary(int(number), padding=padding)
                    number = ""

                last_char = i

                new_line += i
                continue
            
            number += i

        for command in KEYWORDS.keys():
            if command in new_line:
                new_line = new_line.replace(command, KEYWORDS.get(command))

        new_line = new_line.replace(" ", "").replace("r", "").replace("l", "")
        
        if len(new_line) > 15 and "xxxx" in new_line:
            new_line = new_line.replace("xxxx", new_line[16:])
            new_line = new_line[:16]

        new_line = new_line.replace("?", "")

        machine_code_lines.append(new_line)

    print("Done")

    return machine_code_lines

def compile_keywords(keywords = KEYWORDS):
    changed = False
    new_data = {}
    for key, value in keywords.items():
        for k, v in keywords.items():
            if k in value:
                changed = True
                value = value.replace(k, v)
        new_data[key] = value

    if changed:
        new_data = compile_keywords(keywords = new_data)

    return new_data

def main():
    global KEYWORDS

    print("Reading program...", end="")

    with open(TARGET) as f:
        program = f.read()
    
    print("Done")
    start = time.time()
    print(f"Compiling started at: {datetime.datetime.now()}")
    print("Compiling keywords...", end="")

    KEYWORDS = compile_keywords()

    print("Done")

    machine_code = compile_file(program)

    print("Validating code...", end="")
    problems = validator.validate_compiled_code(machine_code)
    if len(problems) != 0 and not FORCE_BUILD:
        for i in problems: print("[ERROR] " + i)

        print(f"Your code has {len(problems)} problems. Either fix them or run the compiler with --force")

        error_path = os.path.abspath("errors.txt")

        with open("errors.txt", "w") as f:
            f.writelines(problems)

        print(f"Build failed at {datetime.datetime.now()}, errors can be found at {error_path}")
        return

    print("Done")

    print("Outputting machine code...", end="")
    rom.output_rom(machine_code, TARGET.removesuffix(".asm"))
    print("Done")

    print(f"Successfully built {TARGET} in {time.time() - start}s with force build {'enabled' if FORCE_BUILD else 'disabled'}")

if __name__ == "__main__":
    main()