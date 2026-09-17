from PyCPU.components.memory import Memory
from PyCPU.components.register import Register
import pytest

R0 = Register("R0")
R0.value = 0x00

R1 = Register("R1")
R1.value = 0x00

def test_write_to_memory():
    mem = Memory(bits=8, size=2)
    mem.write(memory_address=R0, value=0xFF)
    assert mem.data[0] == 0xFF
    assert mem.data[1] == -1

def test_write_to_invalid_memory_too_large():
    mem = Memory(bits=8, size=2)
    R1.value = 0x03
    with pytest.raises(ValueError, match="Address should be less than 2"):
        mem.write(memory_address=R1, value=0xFF)
    assert mem.data[0] == -1
    assert mem.data[1] == -1

def test_write_to_invalid_memory_too_low():
    mem = Memory(bits=8, size=2)
    R1.value = -1
    with pytest.raises(ValueError, match="Address should be >= 0"):
        mem.write(memory_address=R1, value=0xFF)
    assert mem.data[0] == -1
    assert mem.data[1] == -1   

def test_read_to_memory():
    mem = Memory(bits=8, size=2)
    mem.data[0] = 0xFF
    assert mem.read(R0) == 0xFF

def test_read_to_invalid_memory_too_large():
    mem = Memory(bits=8, size=2)
    R1.value = 0x03
    with pytest.raises(ValueError, match="Address should be less than 2"):
        mem.read(R1)

def test_read_to_invalid_memory_too_low():
    mem = Memory(bits=8, size=2)
    R1.value = -1
    with pytest.raises(ValueError, match="Address should be >= 0"):
        mem.read(R1)

def test_read_to_uninitialized():
    mem = Memory(bits=8, size=2)
    with pytest.raises(ValueError, match="Trying to access un-initalized memory at 0"):
        mem.read(R0)

def test_memory_overflow_wraps():
    mem = Memory(bits=8, size=2)
    
    mem.write(R0, 256)
    assert mem.read(R0) == 0