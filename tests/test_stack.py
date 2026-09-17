import pytest
from PyCPU.components.cpu import CPU


def test_push_pop_lifo():
    cpu = CPU(3, memory_size=256)

    cpu.load_program([
        ("MOV", "R0", 10),
        ("MOV", "R1", 20),

        ("PUSH", "R0"),
        ("PUSH", "R1"),

        ("POP", "R2"),
        ("POP", "R0"),
    ])

    cpu.execute()

    assert cpu.registers["R2"].get() == 20
    assert cpu.registers["R0"].get() == 10
    assert cpu.sp == 256

def test_push_decrements_sp():
    cpu = CPU(1, memory_size=256)

    cpu.load_program([
        ("MOV", "R0", 42),
        ("PUSH", "R0"),
    ])

    cpu.execute()

    assert cpu.sp == 255
    assert cpu.memory.data[255] == 42