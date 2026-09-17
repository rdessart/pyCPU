from .register import Register 
from .memory import Memory

class CPU: 
    def __init__(self, register_count: int = 10, bits = 8, memory_size = 256):
        self.registers = {f"R{i}": Register(f"R{i}", bits=bits) for i in range(register_count)}
        self.memory = Memory(size=memory_size, bits=bits)
        self.pc = 0 #program counter
        self.sp = self.memory.size #stack pointer

        self.zero_flag = False
        self.greater_flag = False
        self.less_flag = False
        self.program = []
        self.halted = False

    def __repr__(self):
        out_str = f"CPU INFO:\n\t*PROGRAM LENGTH: {len(self.program)}\n\t*PC: {self.pc}"
        if len(self.program) > 0 and self.pc < len(self.program):
            out_str += f" - OP: {self.program[self.pc]}"
        elif len(self.program) > 0 and self.pc >= len(self.program):
            out_str += " - OP: END"
        else:
            out_str += " - OP: N/A"
        out_str += f"\n\t*ZF: {self.zero_flag}\n\t"
        out_str += f"*GF: {self.greater_flag}\n\t"
        out_str += f"*LF: {self.less_flag}"
        out_str += f"\n\t*REGISTERS: {len(self.registers)}"
        for r in self.registers.values():
            out_str += f"\n\t\t*{r.id} - {r.value} = 0x{r.value:X}"

        return out_str
    
    def load_program(self, excutable: list[tuple]):
        """Reset execution pointer and load an executable"""
        self.pc = 0
        self.program = list(excutable)
        self.halted = False

    def resolve_operand(self, operand):
        """resolve operand"""
        if isinstance(operand, str) and operand.startswith("R"):
            return self.find_register(operand)
        return operand

    def find_register(self, name: str) -> Register:
        """Try to find matching register"""
        try:
            return self.registers[name]
        except KeyError:
            raise ValueError(f"Unknown register: {name}")

    def execute(self):
        """execute program loaded"""
        while self.step():
            pass

    def step(self) -> bool:
        """move one step into program execution"""
        if self.pc >= len(self.program) or self.halted:
            return False
        #To be use if switching to an UI to allow set by set executions
        instruction = self.program[self.pc]
        self.pc += 1
        op = instruction[0]
        args = [self.resolve_operand(args) for args in instruction[1:]]
        self.execute_op(op, *args)
        return True

    def reset(self):
        """reset CPU state, register"""
        self.pc = 0
        self.zero_flag = False
        self.less_flag = False
        self.greater_flag = False
        self.halted = False

        for register in self.registers.values():
            register.set(0)

    def execute_op(self, op: str, *args):
        """execute one single operation"""
        match op.upper():
            case "MOV":
                self._mov(*args)

            case "JUMP":
                self._jump(*args)

            case "CMP":
                self._cmp(*args)

            case "JG":
                self._jg(*args)

            case "JL":
                self._jl(*args)

            case "JE":
                self._je(*args)

            case "ADD":
                self._add(*args)

            case "SUB":
                self._sub(*args)

            case "MUL":
                self._mul(*args)
            
            case "DIV":
                self._div(*args)

            case "NOP":
                pass

            case "HALT":
                self._halt()

            case "LOAD":
                self._load(*args)

            case "STORE":
                self._store(*args)

            case "PUSH":
                self._push(*args)

            case "POP":
                self._pop(*args)

            case _:
                raise ValueError(f"Unknown instruction: {op}")

    def _cmp(self, left: Register, right):
        """compare left and right"""
        right_value = right.get() if isinstance(right, Register) else int(right)
        result = left.get() - right_value
        self.zero_flag = result == 0
        self.greater_flag = result > 0
        self.less_flag = result < 0

    def _mov(self, destination: Register, source):
        """move source into destination"""
        value = source.get() if isinstance(source, Register) else int(source)
        destination.set(value)

    def _add(self, destination: Register, source):
        """add destination by source"""
        value = source.get() if isinstance(source, Register) else int(source)
        destination.add(value)

    def _sub(self, destination: Register, source):
        """substract destination by source"""
        value = source.get() if isinstance(source, Register) else int(source)
        destination.sub(value)

    def _mul(self, destination: Register, source):
        """multiply destination by source"""
        value = source.get() if isinstance(source, Register) else int(source)
        destination.mul(value)

    def _div(self, destination: Register, source):
        """divide destination by source"""
        value = source.get() if isinstance(source, Register) else int(source)
        destination.div(value)

    def _jump(self, address: int):
        """Jump to address"""
        if not 0 <= address < len(self.program):
            raise ValueError(f"Invalid jump address: {address}")
        self.pc = address

    def _jg(self, address: int):
        """Jump if greater to address"""
        if self.greater_flag:
            self._jump(address)

    def _je(self, address: int):
            """Jump if equal to address"""
            if self.zero_flag:
                self._jump(address)

    def _jl(self, address: int):
        """Jump if less to address"""
        if self.less_flag:
            self._jump(address)
    
    def _store(self, memory_address: Register, source: Register):
        """Store register into RAM"""
        if not isinstance(memory_address, Register):
            raise ValueError("STORE memory_address should reference a register")
        if not isinstance(source, Register):
            raise ValueError("STORE source should reference a register")
        self.memory.write(memory_address.get(), source.get())

    def _load(self, destination: Register, memory_address: Register):
        """Load RAM value into register"""
        if not isinstance(memory_address, Register):
            raise ValueError("STORE memory_address should reference a register")
        if not isinstance(destination, Register):
                raise ValueError("LOAD destination should reference a register")
        val = self.memory.read(memory_address.get())
        destination.set(val)

    def _halt(self):
        """Set CPU State to halted"""
        self.halted = True

    def _push(self, source: Register):
        if not isinstance(source, Register):
            raise ValueError("PUSH should reference a register")
        value = source.get()
        self.sp -= 1
        self.memory.write(self.sp, value)

    def _pop(self, destination: Register):
        if not isinstance(destination, Register):
            raise ValueError("POP should reference a register")
        value: int = self.memory.read(self.sp)
        self.sp += 1
        destination.set(value)

