
class Assembler:
    def __init__(self):
        self.labels: dict[str, int] = {}

    def load_program(self, source_code: list[tuple]) -> list[tuple]:
        """ Load a parse a program to return full assembly code"""
        self.labels.clear()
        self.compiled_program.clear()

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
            self.compiled_program.append(instruction)
            address += 1
        #second pass:
        executable = []
        for instruction in self.compiled_program:
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
            executable.append((op, *args))
        return self.executable
