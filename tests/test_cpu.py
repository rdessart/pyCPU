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

    assert cpu.registers["R0"].get() == 10
    assert cpu.registers["R1"].get() == 1

def test_cpu_register_add():
    cpu = CPU(2)
    source = [
            ("MOV", "R0", 10),
            ("MOV", "R1", 1),
            ("ADD", "R1", "R0")
        ]
    cpu.load_program(source)
    cpu.execute()

    assert cpu.registers["R0"].get() == 10
    assert cpu.registers["R1"].get() == 11

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