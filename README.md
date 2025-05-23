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

# Instructions
| Instruction | Docs                                                                                                                                                                                                                                                                              |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `NOP`       | No operation                                                                                                                                                                                                                                                                      |
| `HLT`       | Halt (Stop the clock)                                                                                                                                                                                                                                                             |
| `ADD`       | Add two numbers and store them (`ADD r1 r2 r3` is `r1 + r2 -> r3`)                                                                                                                                                                                                                |
| `SUB`       | Subtract number 1 from number 2 (`SUB r1 r2 r3` is `r1 - r2 -> r3`)                                                                                                                                                                                                               |
| `MOV`       | Move value between registers (`MOV r1 r2` is `r1 -> r2`)                                                                                                                                                                                                                          |
| `RSH`       | Right shift number and store it (`RSH r1 r2` is `r1 >> 1 -> r2`)                                                                                                                                                                                                                  |
| `NOR`       | Bitwise NOR (`NOR r1 r2 r3` is `!(r1 V r2)`)                                                                                                                                                                                                                                      |                                                                                                                                                                                                                                        | r2)`)
| `AND`       | Bitwise AND (`AND r1 r2 r3` is `r1 & r2 -> r3`)                                                                                                                                                                                                                                   |
| `XOR`       | Bitwise XOR (`XOR r1 r2 r3` is `r1 ^ r2 -> r3`)                                                                                                                                                                                                                                   |
| `LDI`       | Load Immediate (`LDI r1 1` is `1 -> r1`)                                                                                                                                                                                                                                          |
| `ADI`       | Add Immediate (`ADI r1 1` is `r1 + 1 -> r1`)                                                                                                                                                                                                                                      |
| `INC`       | Increment (`INC r1` is `r1 + 1 -> r1`)                                                                                                                                                                                                                                            |
| `DEC`       | Decrement (`DEC r1` is `r1 + 255 -> r1` or `r1 - 1 -> r1`)                                                                                                                                                                                                                        |
| `JMP`       | Jump - Unconditional (`JMP always l1` when this line is reached, program jumps to line 1), Conditional - the program jumps to the specified line if the condition is met (`JMP zero l5`), keywords - `always`, `never`, `zero`, `!zero`, `carry`, `!carry`, `==`, `!=`, `>=`, `<` |
| `CMP`       | Compare two numbers, the result can be used in a conditional Jump (`CMP r1 r2` compare r1 and r2, store the result in the ALU flags)                                                                                                                                              |
| `define`    | Define a value not containing a number (`define example example_value`)                                                                                                                                                                                                           |
| `ndefine`   | Define a number (`ndefine example example_number`)                                                                                                                                                                                                                                |
| `.`         | Define a label used in a jump instead of line (`.example_label`, then later you can use something like `JMP always example_label`)                                                                                                                                                |
| `CAL`       | Call a function (`CAL example_label` jumps to that label and stores where should it return); Calls can be only 16 layers deep - the call stack has only 16 layers                                                                                                                 |
| `RET`       | Return from a function (`RET` jumps to the stored line and pops the call stack)                                                                                                                                                                                                   |
| `LOD`       | Load a value from memory to register (`LOD r0 r1 n5` - Load a value from memory address 5 (0 (`r0`) + 5 (`n5`)) to register 1)                                                                                                                                                    |
| `STR`       | Store a value from register to memory (`STR r0 r1 n3` - Store a value from RAM address 3 (`r0` + `n3`) to register 1)                                                                                                                                                             |

[>>> Low-level instructions spreadsheet <<<](https://docs.google.com/spreadsheets/d/1LUdcMzXBbyvQ7C-92FkX6OZsNRdaSb_byfD6Byjk5o8/edit?usp=sharing)