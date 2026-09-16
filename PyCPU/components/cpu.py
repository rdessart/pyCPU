from .register import Register 

class CPU: 
    def __init__(self, register_count: int = 10):
        self.registers = {f"R{i}": Register(f"R{i}") for i in range(register_count)}
        self.pc = 0
        self.labels: dict[str, int] = {}

        self.zero_flag = False
        self.greater_flag = False
        self.less_flag = False
        self.program = []

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


    # Biggest change: we pass from an interpreter mode to a full compilation
    # mode as we need to pass at least one to check for labels in the code
    def load_program(self, source_code: list[tuple]):
        #reset:
        self.pc = 0
        self.labels.clear()
        self.program.clear()

        #first pass:
        address = 0
        for instruction in source_code:
            if instruction[0].upper() == "LABEL":
                if len(instruction) != 2:
                    raise ValueError("LABEL expects exactly one argument")
                label = instruction[1]
                if label in self.labels:
                    raise ValueError(f"Duplicate label : {label}")
                self.labels[label] = address
                continue
            self.program.append(instruction)
            address += 1
        #second pass:
        resolved_program = []
        for instruction in self.program:
            op = instruction[0].upper()
            args = list(instruction[1:])
            if op in ("JUMP", "JG", "JL", "JE"):
                if len(args) != 1:
                    raise ValueError(f"{op} expects one argument")
                target = args[0]
                if isinstance(target, str):
                    if target not in self.labels:
                        raise ValueError(f"Unknown label: {target}")
                    args[0] = self.labels[target]
            resolved_program.append((op, *args))
        self.program = resolved_program

    def resolve_operand(self, operand):
        if isinstance(operand, str) and operand.startswith("R"):
            return self.find_register(operand)
        return operand

    def find_register(self, name: str) -> Register:
        try:
            return self.registers[name]
        except KeyError:
            raise ValueError(f"Unknown register: {name}")

    def execute(self):
        while self.step():
            pass

    def step(self) -> bool:
        if self.pc >= len(self.program):
            return False
        #To be use if switching to an UI to allow set by set executions
        instruction = self.program[self.pc]
        self.pc += 1
        op = instruction[0]
        args = [self.resolve_operand(args) for args in instruction[1:]]
        self.execute_op(op, *args)
        return True

    def execute_op(self, op: str, *args):
        match op.upper():
            case "MOV":
                self.mov(*args)

            case "JUMP":
                self.jump(*args)

            case "CMP":
                self.cmp(*args)

            case "JG":
                self.jg(*args)

            case "JL":
                self.jl(*args)

            case "JE":
                self.je(*args)

            case "ADD":
                self.add(*args)

            case "SUB":
                self.sub(*args)

            case "MUL":
                self.mul(*args)
            
            case "DIV":
                self.div(*args)

            case "NOP":
                pass

            case _:
                raise ValueError(f"Unknown instruction: {op}")

    def cmp(self, left: Register, right):
            right_value = right.get() if isinstance(right, Register) else int(right)
            result = left.get() - right_value
            self.zero_flag = result == 0
            self.greater_flag = result > 0
            self.less_flag = result < 0

    def mov(self, destination: Register, source):
        value = source.get() if isinstance(source, Register) else int(source)
        destination.set(value)

    def add(self, destination: Register, source):
        value = source.get() if isinstance(source, Register) else int(source)
        destination.add(value)

    def sub(self, destination: Register, source):
        value = source.get() if isinstance(source, Register) else int(source)
        destination.sub(value)

    def mul(self, destination: Register, source):
            value = source.get() if isinstance(source, Register) else int(source)
            destination.mul(value)

    def div(self, destination: Register, source):
        value = source.get() if isinstance(source, Register) else int(source)
        destination.div(value)

    def jump(self, address: int):
        if not 0 <= address < len(self.program):
            raise ValueError(f"Invalid jump address: {address}")
        self.pc = address

    def jg(self, address: int):
        if self.greater_flag:
            self.jump(address)

    def je(self, address: int):
            if self.zero_flag:
                self.jump(address)

    def jl(self, address: int):
        if self.less_flag:
            self.jump(address)