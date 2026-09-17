from PyCPU.components.cpu import CPU
from PyCPU.program.assembler import Assembler

if __name__ == "__main__":
    cpu = CPU(6)
    assembler = Assembler()

# def fib(n):
#     if n <= 1:
#         return n
#     return fib(n - 1) + fib(n - 2)

# for i in range(7):
#     print(fib(i), end=" ")

    program = [
    # MAIN
    ("MOV", "R0", 5),        # n = 5
    ("CALL", "FIB"),          # R0 = fib(5)
    ("MOV", "R3", "R0"),     # save result
    ("HALT",),

    # --------------------------------
    # FIB
    # Input:  R0 = n
    # Output: R0 = fib(n)
    # --------------------------------
    ("LABEL", "FIB"),

    # if n < 2:
    #     return n
    ("CMP", "R0", 2),
    ("JL", "FIB_BASE"),

    # Save n because we're about to modify R0
    ("PUSH", "R0"),

    # fib(n - 1)
    ("SUB", "R0", 1),
    ("CALL", "FIB"),

    # R0 now contains fib(n - 1)
    ("MOV", "R1", "R0"),

    # Restore original n
    ("POP", "R0"),

    # Save fib(n - 1), because the next recursive call
    # is allowed to modify R1
    ("PUSH", "R1"),

    # fib(n - 2)
    ("SUB", "R0", 2),
    ("CALL", "FIB"),

    # R0 now contains fib(n - 2)

    # Restore fib(n - 1)
    ("POP", "R1"),

    # fib(n) = fib(n - 2) + fib(n - 1)
    ("ADD", "R0", "R1"),

    ("RET",),

    # Base case: fib(0) = 0, fib(1) = 1
    ("LABEL", "FIB_BASE"),
    ("RET",),
    ]

    executable = assembler.assemble(program)
    cpu.load_program(executable)
    while cpu.step():
        print(cpu)
        if(cpu.sp <= 255):
            print(f"SP : {cpu.sp} - {cpu.memory.data[cpu.sp]:X}")
        else:
            print(f"SP : {cpu.sp}")

