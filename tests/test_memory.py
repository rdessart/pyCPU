from PyCPU.components.memory import Memory
import pytest

def test_write_to_memory():
    mem = Memory(bits=8, size=2)
    mem.write(memory_address=0, value=0xFF)
    assert mem.data[0] == 0xFF
    assert mem.data[1] == -1

def test_write_to_invalid_memory_too_large():
    mem = Memory(bits=8, size=2)
    with pytest.raises(ValueError, match="Address should be less than 2"):
        mem.write(memory_address=3, value=0xFF)
    assert mem.data[0] == -1
    assert mem.data[1] == -1

def test_write_to_invalid_memory_too_low():
    mem = Memory(bits=8, size=2)
    with pytest.raises(ValueError, match="Address should be >= 0"):
        mem.write(memory_address=-1, value=0xFF)
    assert mem.data[0] == -1
    assert mem.data[1] == -1   

def test_read_to_memory():
    mem = Memory(bits=8, size=2)
    mem.data[0] = 0xFF
    assert mem.read(0) == 0xFF

def test_read_to_invalid_memory_too_large():
    mem = Memory(bits=8, size=2)
    with pytest.raises(ValueError, match="Address should be less than 2"):
        mem.read(3)

def test_read_to_invalid_memory_too_low():
    mem = Memory(bits=8, size=2)
    with pytest.raises(ValueError, match="Address should be >= 0"):
        mem.read(-1)

def test_read_to_uninitialized():
    mem = Memory(bits=8, size=2)
    with pytest.raises(ValueError, match="Trying to access un-initalized memory at 0"):
        mem.read(0)

def test_memory_overflow_wraps():
    mem = Memory(bits=8, size=2)
    
    mem.write(0, 256)
    assert mem.read(0) == 0