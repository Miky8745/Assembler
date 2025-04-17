# Assembler
This is an assembler for a 8bit computer I built inside Sebastian Lague's Simulation (https://github.com/SebLague/Digital-Logic-Sim)

# Installation
1. Download this repo
2. Run the `Digital-Logic-Sim.exe` in `Computer/Digital-Logic-Sim-Windows/Digital-Logic-Sim`
3. Close the application
4. Copy the `Computer` under `Computer/Project` to `C:\Users\<Your Name>\AppData\LocalLow\SebastianLague\Digital-Logic-Sim\Projects`
5. Run the application again and open the Computer project

# Running the compiler
1. Make your own script and give it a name ending with `.asm`
2. Run `python compiler.py <filename>.asm`
3. If you have a mistake anywhere, it will tell you, if you believe it is not your fault and the compiler's validator is bugged, or want to see how invalid machine code looks, you can run it with the `--force` flag
4. When you have the two files of machine code (`<filename>_a.bin` and `<filename>_b.bin`), copy the outputs into the ROM inside `Inst-Memory` chip

# Running the computer
Once you have the machine code inside the ROM of the `Inst-Memory`, go back to the `Computer` chip and hit the `RESET` button, after that, turn off the `RESET` button and hit `START`. When the computer reaches the `HLT` instruction, it will automatically stop