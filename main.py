from cpu import CPU


if __name__ == "__main__":
    cpu = CPU(2)

    program = [
        ("MOV", "R0", 10),    # 0
        ("MOV", "R1", 1),     # 1

        ("SUB", "R0", "R1"),  # 2
        ("CMP", "R0", 0),     # 3
        ("JG", 2),             # 4
    ]
    cpu.load_program(program)
    while cpu.step():
        print(cpu)

