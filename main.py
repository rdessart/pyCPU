from PyCPU.components.cpu import CPU
from PyCPU.program.assembler import Assembler

if __name__ == "__main__":
    cpu = CPU(4)
    assembler = Assembler()

    program = [
        ("MOV", "R0", 10),    # 0
        ("MOV", "R1", 5),     # 1
        ("MOV", "R2", 2), #address
        ("PUSH", "R0"),
        ("PUSH", "R1"),
        ("PUSH", "R2"),
        ("MOV", "R0", 0),
        ("MOV", "R1", 0),
        ("MOV", "R2", 0),
        ("POP", "R2"),
        ("POP", "R1"),
        ("POP", "R0"),
    ]
    executable = assembler.assemble(program)
    cpu.load_program(executable)
    while cpu.step():
        print(cpu)
        if(cpu.sp <= 255):
            print(f"SP : {cpu.sp} - {cpu.memory.data[cpu.sp]:X}")
        else:
            print(f"SP : {cpu.sp}")
    print(cpu.memory)

