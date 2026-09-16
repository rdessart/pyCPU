from PyCPU.components.cpu import CPU
from PyCPU.program.assembler import Assembler

if __name__ == "__main__":
    cpu = CPU(4)
    assembler = Assembler()

    program = [
        ("MOV", "R0", 10),    # 0
        ("MOV", "R1", 0),     # 1
        ("MOV", "R2", 0), #address
        ("LABEL", "LOOP"),
        ("SUB", "R0", 1),  # 2
        ("ADD", "R1", 5),
        ("CMP", "R0", 0),     # 3
        ("JG", "LOOP"),       # 4
        ("STORE", "R2", "R1"),
        ("MOV", "R1", 0),
        ("LOAD", "R1", "R2"),
    ]
    executable = assembler.assemble(program)
    cpu.load_program(executable)
    while cpu.step():
        print(cpu)
    print(cpu.memory)

