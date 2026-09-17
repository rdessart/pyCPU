from .register import Register

class Memory:
    """Represent memory"""
    def __init__(self, size:int = 256, bits: int = 8):
        self.size = size
        self.bits = bits
        self.mask = (1 << bits) - 1
        self.data = [-1] * size #made it -1 to better see un-initialized memory

    def __repr__(self):
        out_str = ""
        for i, data in enumerate(self.data):
            out_str += f"[{i}] = {data}\n"
        return out_str

    def resolve_memory_address(self, address: Register) -> int:
        if not isinstance(address, Register):
            raise ValueError("memory address should be a pointer!")
        memory_address = address.get()
        self._validate_address(memory_address)
        return memory_address

    def read(self, memory_address: Register) -> int:
        address = self.resolve_memory_address(memory_address)
        if self.data[address] < 0:
            raise ValueError(f"Trying to access un-initalized memory at {address}")
        return self.data[address]

    def write(self, memory_address: Register, value: int):
        address = self.resolve_memory_address(memory_address)
        self.data[address] = value & self.mask

    def _validate_address(self, address: int):
        if address < 0:
            raise ValueError("Address should be >= 0")
        if address >= self.size:
            raise ValueError(f"Address should be less than {self.size}")
        