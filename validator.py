def validate_compiled_code(machine_code):
    problems = []

    if len(machine_code) > 2**16:
        problems.append(f"Machine code is too long ({len(machine_code)}/{2**16})\n")

    for index, line in enumerate(machine_code):
        if len(line) > 16:
            problems.append(f"Line {index+1} is too long ({len(line)}/{16})\n")
        elif len(line) < 16:
            problems.append(f"Line {index + 1} is too short ({len(line)}/{16})\n")

        for j in line:
            if j != "0" and j != "1":
                problems.append(f"Found an invalid character ({str(j)}) at line {index+1}\n")

    return problems