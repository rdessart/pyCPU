class Register:
    def __init__(self, id: str, bits: int = 8):
        self.id = id
        self.value = 0x00
        self.bits = bits

    @property
    def mask(self):
        return (1 << self.bits) - 1

    def set(self, value: int):
        self.value = value & self.mask
        print(self)

    def get(self):
        return self.value

    def __repr__(self):
        return f"{self.id} hold {self.value} (0x{self.value:X})"

    def add(self, value: int):
       self.set(self.value + value)

    def sub(self, value: int):
        self.set(self.value - value)

    def mul(self, value: int):
         self.set(self.value * value)

    def div(self, value: int):
        if value == 0:
            raise ZeroDivisionError("CPU division by zero")
        
        self.set(self.value // value)

    def move(self, value: int):
        self.set(value)