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
        # Call stack for function calls
        self.call_stack = []
        # Parameters buffer for function calls
        self.params = []
        # Function metadata: maps function label to parameter names
        self.function_params = {}
        # build label -> ip map
        self.labels = {}
        for idx, instr in enumerate(self.code):
            if instr[0] == 'label':
                self.labels[instr[1]] = idx
                # Check if next instruction is a PARAMS comment
                if idx + 1 < len(self.code) and self.code[idx + 1][0] == ';':
                    # Parse parameter names from comment
                    comment = self.code[idx + 1][1][0] if self.code[idx + 1][1] else ''
                    if comment.startswith('PARAMS '):
                        params_str = comment[7:]  # Remove 'PARAMS ' prefix
                        param_names = [p.strip() for p in params_str.split(',')]
                        self.function_params[instr[1]] = param_names

    def run(self):
        while self.ip < len(self.code):
            instr = self.code[self.ip]
            op = instr[0]
            args = instr[1]
            # advance by default
            self.ip += 1
            if op == 'label':
                continue
            if op == ';':
                # Comment, skip
                continue
            if op == 'PUSH':
                val = args[0]
                # Check if it's a string literal (starts and ends with quotes)
                if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
                    # Store the string without quotes
                    self.stack.append(val[1:-1])
                else:
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
            if op == 'MOD':
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a % b if b != 0 else 0)
                continue
            if op in ('LT','GT','LE','GE','EQ','NE','AND','OR'):
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
                elif op == 'NE':
                    res = 1 if a != b else 0
                elif op == 'AND':
                    res = 1 if (a != 0 and b != 0) else 0
                elif op == 'OR':
                    res = 1 if (a != 0 or b != 0) else 0
                self.stack.append(res)
                continue
            if op == 'NOT':
                a = self.stack.pop()
                res = 1 if a == 0 else 0  # NOT: 0 becomes 1, non-zero becomes 0
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
                import sys
                print(f"Ingrese valor para {name}: ", end='', flush=True)
                try:
                    v = int(input())
                except Exception:
                    v = 0
                self.vars[name] = v
                continue
            if op == 'OUT':
                val = self.stack.pop() if self.stack else 0
                print(val)
                continue
            if op == 'PARAM':
                # Pop value from stack and add to parameters list
                val = self.stack.pop() if self.stack else 0
                self.params.append(val)
                continue
            if op == 'CALL':
                # CALL FUNC_name num_params
                func_label = args[0]
                num_params = int(args[1]) if len(args) > 1 else 0
                # Get parameters from params buffer
                call_params = self.params[-num_params:] if num_params > 0 else []
                # Save return address and local variables
                self.call_stack.append({
                    'return_ip': self.ip,
                    'saved_vars': self.vars.copy(),
                })
                # Clear params buffer (keep only the ones not used)
                if num_params > 0:
                    self.params = self.params[:-num_params]
                # Set up new local scope with parameters
                self.vars = {}
                # Assign parameters to local variables
                param_names = self.function_params.get(func_label, [])
                for i, param_name in enumerate(param_names):
                    if i < len(call_params):
                        self.vars[param_name] = call_params[i]
                # Jump to function
                self.ip = self.labels.get(func_label, self.ip)
                continue
            if op == 'RET':
                # Pop return value from stack (if any)
                return_value = self.stack.pop() if self.stack else 0
                # Restore caller's context
                if self.call_stack:
                    frame = self.call_stack.pop()
                    self.ip = frame['return_ip']
                    self.vars = frame['saved_vars']
                    # Push return value back onto stack
                    self.stack.append(return_value)
                else:
                    # No call stack means we're at the end of program
                    return
                continue
            # Unknown ops: ignore
            # print('VM: unknown op', op, args)
        # finished
        return
