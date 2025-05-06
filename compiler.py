import datetime
import json
import os
import sys
import time

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
    "n": 4,
    "l": 9
}

NUMBER_DEFINITIONS = {}

def convert_binary(number : int, padding = 4):
    default_conversion = bin(number)[2:]

    if padding is None:
        padding = 0
    
    return "0" * (padding - len(default_conversion)) + default_conversion

def compile_file(lines : list[str]):
    machine_code_lines = []

    for line in lines:
        if len(line.strip()) < 2 or line[0] == "#":
            continue

        for number in NUMBER_DEFINITIONS.keys():
            if number in line:
                line = line.replace(number, NUMBER_DEFINITIONS.get(number))

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

        for i in PADDING.keys():
            new_line = new_line.replace(i, "")
        
        if len(new_line) > 15 and "xxxx" in new_line:
            new_line = new_line.replace("xxxx", new_line[16:])
            new_line = new_line[:16]

        new_line = new_line.replace("?", "")

        machine_code_lines.append(new_line)

    return machine_code_lines

def find_user_definitions(code: list[str]):
    global KEYWORDS, NUMBER_DEFINITIONS

    real_code = []

    for i in code:
        if "define" in i[:10]:
            keyword, value = i.split()[1:3]
            
            if "ndefine" in i[:10]:
                NUMBER_DEFINITIONS[keyword] = value
                continue

            KEYWORDS[keyword] = value
            continue

        if len(i.strip()) < 2 or i.strip()[0] == "#":
            continue

        elif len(i) > 1 and "." == i[0]:
            NUMBER_DEFINITIONS[i.split(" ")[0][1:]] = f"l{len(real_code)+1}"
            continue

        real_code.append(i)

    keys = sorted(NUMBER_DEFINITIONS.keys(), key=len, reverse=True)
    NUMBER_DEFINITIONS = {k: NUMBER_DEFINITIONS[k] for k in keys}
    
    keys = sorted(KEYWORDS.keys(), key=len, reverse=True)
    KEYWORDS = {k: KEYWORDS[k] for k in keys}

    return real_code

def compile_keywords(keywords):
    changed = False
    new_data = {}
    for key, value in keywords.items():
        for k, v in keywords.items():
            if k in value:
                changed = True
                value = value.replace(k, v)
        new_data[key] = value

    if changed:
        new_data = compile_keywords(new_data)

    return new_data

def step(description, func=None):
    print(f"{description}...", end="")
    result = func() if func else None
    print("Done")
    return result

def main():
    global KEYWORDS, NUMBER_DEFINITIONS

    print(f"Compilation started at: {datetime.datetime.now()}")
    start = time.time()

    program = step("Reading program", lambda: open(TARGET).read())

    program = step("Finding user definitions", lambda: find_user_definitions(program.split("\n")))

    KEYWORDS = step("Compiling keywords", lambda: compile_keywords(KEYWORDS))

    NUMBER_DEFINITIONS = step("Compiling number definitions", lambda: compile_keywords(NUMBER_DEFINITIONS))

    machine_code = step("Compiling code", lambda: compile_file(program))

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

    step("Outputting machine code", lambda: rom.output_rom(machine_code, TARGET.removesuffix(".asm")))

    print(f"Successfully built {TARGET} in {time.time() - start}s with force build {'enabled' if FORCE_BUILD else 'disabled'}")

if __name__ == "__main__":
    main()