"""Generador de ensamblador simbólico para una máquina ficticia.

Traduce TAC a instrucciones simbólicas tipo: LOAD, STORE, ADD, SUB, MUL, DIV, JMP, JLT, ...
"""
from typing import List


def is_number(s):
    """Check if a string represents a number (including negative)."""
    try:
        int(s)
        return True
    except ValueError:
        return False


def generate_asm(tac_list) -> List[str]:
    asm: List[str] = []
    # We'll treat temps like named variables (t1,t2,...)
    for instr in tac_list:
        if instr.op == 'label':
            asm.append(f"{instr.a}:")
        elif instr.op == 'goto':
            asm.append(f"JMP {instr.a}")
        elif instr.op == 'read':
            asm.append(f"IN {instr.a}")
        elif instr.op == 'print':
            src = instr.a
            # load value and out
            if src.startswith('"') and src.endswith('"'):
                # String literal
                asm.append(f"PUSH {src}")
            elif is_number(src):
                asm.append(f"PUSH {src}")
            else:
                asm.append(f"LOAD {src}")
            asm.append("OUT")
        elif instr.op == 'assign':
            target = instr.a
            src = instr.b
            if isinstance(src, str) and (is_number(src) or (src.startswith('"') and src.endswith('"'))):
                asm.append(f"PUSH {src}")
            else:
                asm.append(f"LOAD {src}")
            asm.append(f"STORE {target}")
        elif instr.op == 'binop':
            target = instr.a
            op = instr.b
            left, right = instr.c
            # push left then right
            if isinstance(left, str) and is_number(left):
                asm.append(f"PUSH {left}")
            else:
                asm.append(f"LOAD {left}")
            if isinstance(right, str) and is_number(right):
                asm.append(f"PUSH {right}")
            else:
                asm.append(f"LOAD {right}")
            if op == '+':
                asm.append("ADD")
            elif op == '-':
                asm.append("SUB")
            elif op == '*':
                asm.append("MUL")
            elif op == '/':
                asm.append("DIV")
            elif op == '<':
                asm.append("LT")
            elif op == '>':
                asm.append("GT")
            elif op == '<=':
                asm.append("LE")
            elif op == '>=':
                asm.append("GE")
            elif op == '==':
                asm.append("EQ")
            elif op == '!=':
                asm.append("NE")
            else:
                asm.append(f"; UNKNOWN_OP {op}")
            asm.append(f"STORE {target}")
        elif instr.op == 'ifgoto':
            left = instr.a
            op = instr.b
            right, label = instr.c
            if isinstance(left, str) and left.isdigit():
                asm.append(f"PUSH {left}")
            else:
                asm.append(f"LOAD {left}")
            if isinstance(right, str) and right.isdigit():
                asm.append(f"PUSH {right}")
            else:
                asm.append(f"LOAD {right}")
            # produce condition result
            if op == '<':
                asm.append("LT")
            elif op == '>':
                asm.append("GT")
            elif op == '<=':
                asm.append("LE")
            elif op == '>=':
                asm.append("GE")
            elif op == '==':
                asm.append("EQ")
            elif op == '!=':
                asm.append("NE")
            else:
                asm.append(f"; UNKNOWN_COND {op}")
            # if condition true -> jump
            asm.append(f"JNZ {label}")
        elif instr.op == 'func_start':
            # Mark function start with a label and store param names
            asm.append(f"FUNC_{instr.a}:")
            # Add metadata comment with parameter names
            if instr.b:  # instr.b contains parameter list
                param_list = ','.join(instr.b)
                asm.append(f"; PARAMS {param_list}")
        elif instr.op == 'func_end':
            # Function end - only add RET if no explicit return was just generated
            # (return statement already emits RET)
            # For safety, we can skip this or add a label
            pass
        elif instr.op == 'param':
            # Push parameter onto stack
            src = instr.a
            if isinstance(src, str) and (is_number(src) or (src.startswith('"') and src.endswith('"'))):
                asm.append(f"PUSH {src}")
            else:
                asm.append(f"LOAD {src}")
            asm.append("PARAM")
        elif instr.op == 'call':
            # CALL function_name num_params return_target
            func_name = instr.a
            num_params = instr.b
            return_target = instr.c
            asm.append(f"CALL FUNC_{func_name} {num_params}")
            if return_target:
                asm.append(f"STORE {return_target}")
        elif instr.op == 'return':
            # Push return value and return
            src = instr.a
            if isinstance(src, str) and (is_number(src) or (src.startswith('"') and src.endswith('"'))):
                asm.append(f"PUSH {src}")
            else:
                asm.append(f"LOAD {src}")
            asm.append("RET")
        else:
            asm.append(f"; UNHANDLED_TAC {instr}")
    return asm
