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

def test_stack_overflow():
    cpu = CPU(1, memory_size=2)

    cpu.load_program([
        ("MOV", "R0", 42),
        ("PUSH", "R0"),
        ("PUSH", "R0"),
        ("PUSH", "R0"),
    ])

    with pytest.raises(ValueError, match="STACK OVERFLOW"):
        cpu.execute()

    assert cpu.sp == 0

def test_stack_underflow():
    cpu = CPU(1, memory_size=2)

    cpu.load_program([
        ("POP", "R0"),
    ])

    with pytest.raises(ValueError, match="STACK UNDERFLOW"):
        cpu.execute()

    assert cpu.sp == 2

def test_reset_restores_stack_pointer():
    cpu = CPU(1, memory_size=8)

    cpu.load_program([
        ("MOV", "R0", 42),
        ("PUSH", "R0"),
        ("PUSH", "R0"),
    ])

    cpu.execute()

    assert cpu.sp == 6

    cpu.reset()

    assert cpu.sp == 8

def test_call_ret():
    cpu = CPU(1)

    cpu.load_program([
        ("MOV", "R0", 5),
        ("CALL", 4),
        ("HALT",),
        ("NOP",),
        ("ADD", "R0", "R0"),
        ("RET",),
    ])

    cpu.execute()

    assert cpu.registers["R0"].get() == 10
    assert cpu.sp == cpu.memory.size