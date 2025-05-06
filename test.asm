# Define variables
ndefine remaining_loops r3

# Load values to registers
LDI r2 1
LDI r1 1
LDI remaining_loops 3

CAL compute_fib_seq
HLT

# Fib sequence function
.compute_fib_seq
ADD r1 r2 r1
ADD r1 r2 r2

DEC remaining_loops

CMP remaining_loops r0
JMP != compute_fib_seq

RET