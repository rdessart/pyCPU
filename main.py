from PyCPU.components.cpu import CPU
from PyCPU.program.assembler import Assembler

if __name__ == "__main__":
    cpu = CPU(2)
    assembler = Assembler()

    program = [
        ("MOV", "R0", 10),    # 0
        ("MOV", "R1", 1),     # 1
        ("LABEL", "LOOP"),
        ("SUB", "R0", "R1"),  # 2
        ("CMP", "R0", 0),     # 3
        ("JG", "LOOP"),       # 4
    ]
    executable = assembler.load_program(program)
    cpu.load_program(executable)
    while cpu.step():
        print(cpu)

