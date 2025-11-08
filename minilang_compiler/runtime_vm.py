"""Máquina virtual simple para ejecutar el formato generado por `assemble()`.

El assembler produce una lista donde cada entrada puede ser:
- ('label', name)
- ('PUSH', [value])
- ('LOAD', [var])
- ('STORE', [var])
- ('ADD'/'SUB'/...') with no args
- ('JNZ', [label]) / ('JZ', [label])
- ('IN', [var]) / ('OUT', [])

Esta VM implementa una pila y una memoria de variables.
"""
from typing import List, Tuple, Any


class SimpleVM:
    def __init__(self, code: List[Tuple[Any, list]]):
        self.code = code
        self.ip = 0
        self.stack = []
        self.vars = {}
        # build label -> ip map
        self.labels = {}
        for idx, instr in enumerate(self.code):
            if instr[0] == 'label':
                self.labels[instr[1]] = idx

    def run(self):
        while self.ip < len(self.code):
            instr = self.code[self.ip]
            op = instr[0]
            args = instr[1]
            # advance by default
            self.ip += 1
            if op == 'label':
                continue
            if op == 'PUSH':
                val = args[0]
                try:
                    self.stack.append(int(val))
                except ValueError:
                    # push variable value
                    self.stack.append(self.vars.get(val, 0))
                continue
            if op == 'LOAD':
                name = args[0]
                self.stack.append(self.vars.get(name, 0))
                continue
            if op == 'STORE':
                name = args[0]
                val = self.stack.pop() if self.stack else 0
                self.vars[name] = val
                continue
            if op == 'ADD':
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a + b)
                continue
            if op == 'SUB':
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a - b)
                continue
            if op == 'MUL':
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a * b)
                continue
            if op == 'DIV':
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a // b if b != 0 else 0)
                continue
            if op in ('LT','GT','LE','GE','EQ','NE'):
                b = self.stack.pop(); a = self.stack.pop()
                if op == 'LT':
                    res = 1 if a < b else 0
                elif op == 'GT':
                    res = 1 if a > b else 0
                elif op == 'LE':
                    res = 1 if a <= b else 0
                elif op == 'GE':
                    res = 1 if a >= b else 0
                elif op == 'EQ':
                    res = 1 if a == b else 0
                else:
                    res = 1 if a != b else 0
                self.stack.append(res)
                continue
            if op == 'JNZ':
                label = args[0]
                cond = self.stack.pop() if self.stack else 0
                if cond != 0:
                    # jump to label
                    self.ip = self.labels.get(label, self.ip)
                continue
            if op == 'JZ':
                label = args[0]
                cond = self.stack.pop() if self.stack else 0
                if cond == 0:
                    self.ip = self.labels.get(label, self.ip)
                continue
            if op == 'JMP' or op == 7:
                label = args[0]
                self.ip = self.labels.get(label, self.ip)
                continue
            if op == 'IN':
                name = args[0]
                # simple input via input()
                try:
                    v = int(input(f"IN {name}: "))
                except Exception:
                    v = 0
                self.vars[name] = v
                continue
            if op == 'OUT':
                val = self.stack.pop() if self.stack else 0
                print(val)
                continue
            # Unknown ops: ignore
            # print('VM: unknown op', op, args)
        # finished
        return
