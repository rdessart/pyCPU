from PyCPU.components.cpu import CPU
import pytest

def test_cpu_register_init():
    cpu = CPU(2)
    source = [
            ("MOV", "R0", 10),
            ("MOV", "R1", 1),
        ]
    cpu.load_program(source)
    cpu.execute()

    assert cpu.registers["R0"].value == 10
    assert cpu.registers["R1"].value == 1

def test_cpu_register_add():
    cpu = CPU(2)
    source = [
            ("MOV", "R0", 10),
            ("MOV", "R1", 1),
            ("ADD", "R1", "R0")
        ]
    cpu.load_program(source)
    cpu.execute()

    assert cpu.registers["R0"].value == 10
    assert cpu.registers["R1"].value == 11

def test_cpu_register_cmp_less():
    cpu = CPU(2)
    source = [
            ("MOV", "R0", 10),
            ("MOV", "R1", 1),
            ("CMP", "R1", "R0")
        ]
    cpu.load_program(source)
    cpu.execute()

    assert cpu.zero_flag is False
    assert cpu.less_flag is True
    assert cpu.greater_flag is False

def test_cpu_register_cmp_bigger():
    cpu = CPU(2)
    source = [
            ("MOV", "R0", 10),
            ("MOV", "R1", 1),
            ("CMP", "R0", "R1")
        ]
    cpu.load_program(source)
    cpu.execute()

    assert cpu.zero_flag is False
    assert cpu.less_flag is False
    assert cpu.greater_flag is True

def test_cpu_register_cmp_equal():
    cpu = CPU(2)
    source = [
            ("MOV", "R0", 10),
            ("MOV", "R1", 10),
            ("CMP", "R0", "R1")
        ]
    cpu.load_program(source)
    cpu.execute()

    assert cpu.zero_flag is True
    assert cpu.less_flag is False
    assert cpu.greater_flag is False

def test_step_advances_pc():
    cpu = CPU(1)

    cpu.load_program([
        ("MOV", "R0", 10),
        ("ADD", "R0", 1),
    ])

    assert cpu.pc == 0

    assert cpu.step() is True
    assert cpu.pc == 1
    assert cpu.registers["R0"].get() == 10

    assert cpu.step() is True
    assert cpu.pc == 2
    assert cpu.registers["R0"].get() == 11

    assert cpu.step() is False

def test_jump():
    cpu = CPU(1)

    cpu.load_program([
        ("JUMP", 2),
        ("MOV", "R0", 99),
        ("MOV", "R0", 42),
    ])

    cpu.execute()

    assert cpu.registers["R0"].get() == 42

def test_jump_greater_taken():
    cpu = CPU(1)

    cpu.load_program([
        ("MOV", "R0", 10),
        ("CMP", "R0", 5),
        ("JG", 4),
        ("MOV", "R0", 99),
        ("MOV", "R0", 42),
    ])

    cpu.execute()

    assert cpu.registers["R0"].get() == 42

def test_jump_greater_not_taken():
    cpu = CPU(1)

    cpu.load_program([
        ("MOV", "R0", 1),
        ("CMP", "R0", 5),
        ("JG", 4),
        ("MOV", "R0", 42),
        ("NOP",),
    ])

    cpu.execute()

    assert cpu.registers["R0"].get() == 42

def test_add_overflow_wraps():
    cpu = CPU(1)

    cpu.load_program([
        ("MOV", "R0", 255),
        ("ADD", "R0", 1),
    ])

    cpu.execute()

    assert cpu.registers["R0"].get() == 0

def test_sub_underflow_wraps():
    cpu = CPU(1)

    cpu.load_program([
        ("MOV", "R0", 0),
        ("SUB", "R0", 1),
    ])

    cpu.execute()

    assert cpu.registers["R0"].get() == 255

def test_invalid_jump_raises():
    cpu = CPU(1)

    cpu.load_program([
        ("JUMP", 10),
    ])

    with pytest.raises(ValueError, match="Invalid jump address"):
        cpu.execute()


def test_unassemble_program():
    cpu = CPU(2)
   
    cpu.load_program([
        ("MOV", "R0", 0),
        ("MOV", "R1", 0),

        ("LABEL", "LOOP"),
        ("ADD", "R0", 1),
        ("CMP", "R0", 10),
        ("JL", "LOOP")
    ])

    with pytest.raises(ValueError, match="Unknown instruction: LABEL"):
        cpu.execute()

def test_halting():
    cpu = CPU(2)

    cpu.load_program([
        ("MOV", "R0", 0),
        ("MOV", "R1", 0),
        ("ADD", "R0", 1),
        ("ADD", "R1", 5),
        ("CMP", "R0", 10),
        ("JL", 2)
    ])
    for i in range(10):
        assert cpu.step() == True
    cpu.halt()
    assert cpu.step() == False

def test_reset():
    cpu = CPU(2)

    cpu.load_program([
        ("MOV", "R0", 0),
        ("MOV", "R1", 0),
        ("ADD", "R0", 1),
        ("ADD", "R1", 5),
        ("CMP", "R0", 10),
        ("JL", 2)
    ])
    for i in range(10):
        assert cpu.step() == True
    cpu.reset()
    assert cpu.pc == 0
    assert cpu.zero_flag is False
    assert cpu.less_flag is False
    assert cpu.greater_flag is False

    for reg in cpu.registers.values():
        assert reg.get() == 0