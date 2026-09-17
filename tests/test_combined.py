from PyCPU.program.assembler import Assembler
from PyCPU.components.cpu import CPU
import pytest

def test_recursive_fibonacci():
    cpu = CPU(6)
    assembler = Assembler()

    program = [
        ("MOV", "R0", 5),
        ("CALL", "FIB"),
        ("MOV", "R3", "R0"),
        ("HALT",),

        ("LABEL", "FIB"),
        ("CMP", "R0", 2),
        ("JL", "FIB_BASE"),

        ("PUSH", "R0"),
        ("SUB", "R0", 1),
        ("CALL", "FIB"),
        ("MOV", "R1", "R0"),

        ("POP", "R0"),
        ("PUSH", "R1"),

        ("SUB", "R0", 2),
        ("CALL", "FIB"),

        ("POP", "R1"),
        ("ADD", "R0", "R1"),
        ("RET",),

        ("LABEL", "FIB_BASE"),
        ("RET",),
    ]

    cpu.load_program(assembler.assemble(program))
    cpu.execute()

    assert cpu.registers["R0"].get() == 5
    assert cpu.registers["R3"].get() == 5
    assert cpu.sp == cpu.memory.size
    assert cpu.halted is True