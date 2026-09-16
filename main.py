from PyCPU.components.cpu import CPU
from PyCPU.program.compiler import Compiler

if __name__ == "__main__":
    cpu = CPU(2)
    compiler = Compiler()

    program = [
        ("MOV", "R0", 10),    # 0
        ("MOV", "R1", 1),     # 1
        ("LABEL", "LOOP"),
        ("SUB", "R0", "R1"),  # 2
        ("CMP", "R0", 0),     # 3
        ("JG", "LOOP"),       # 4
    ]
    compiler.load_program(program)
    executable = compiler.compiled_program
    cpu.load_program(executable)
    while cpu.step():
        print(cpu)

