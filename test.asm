ndefine i r1

LDI i 5
LDI r2 3
.iterate
DEC i
CMP i r2
JMP != iterate
HLT