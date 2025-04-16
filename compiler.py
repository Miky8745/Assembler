import datetime
import json
import sys
import time
import os

import rom
import validator

with open("commands.json") as f: COMMANDS = json.load(f)

TARGET = sys.argv[1]
FORCE_BUILD = "--force" in sys.argv

def convert_binary(number : int):
    default_conversion = bin(number)[2:]
    
    return "0" * (4 - len(default_conversion)) + default_conversion

def compile_file(program : str):
    lines = program.split("\n")

    machine_code_lines = []

    print("Compiling...", end="")
    for line in lines:
        new_line = ""
        number = ""
        for i in line+" ":
            if i == "#":
                break

            if not i.isdigit():
                if number != "":
                    new_line += convert_binary(int(number))
                    number = ""

                new_line += i
                continue
            
            number += i

        for command in COMMANDS.keys():
            if command in new_line:
                new_line = new_line.replace(command, COMMANDS.get(command))

        new_line = new_line.replace(" ", "").replace("r", "")

        machine_code_lines.append(new_line)

    print("Done")

    return machine_code_lines

def main():
    print("Reading program...", end="")
    with open(TARGET) as f:
        program = f.read()
    
    print("Done")

    start = time.time()
    print(f"Compiling started at: {datetime.datetime.now()}")
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