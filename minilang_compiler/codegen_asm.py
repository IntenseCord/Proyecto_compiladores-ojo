"""Generador de ensamblador simbólico para una máquina ficticia.

Traduce TAC a instrucciones simbólicas tipo: LOAD, STORE, ADD, SUB, MUL, DIV, JMP, JLT, ...
"""
from typing import List


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
            elif src.isdigit():
                asm.append(f"PUSH {src}")
            else:
                asm.append(f"LOAD {src}")
            asm.append("OUT")
        elif instr.op == 'assign':
            target = instr.a
            src = instr.b
            if isinstance(src, str) and (src.isdigit() or (src.startswith('"') and src.endswith('"'))):
                asm.append(f"PUSH {src}")
            else:
                asm.append(f"LOAD {src}")
            asm.append(f"STORE {target}")
        elif instr.op == 'binop':
            target = instr.a
            op = instr.b
            left, right = instr.c
            # push left then right
            if isinstance(left, str) and left.isdigit():
                asm.append(f"PUSH {left}")
            else:
                asm.append(f"LOAD {left}")
            if isinstance(right, str) and right.isdigit():
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
        else:
            asm.append(f"; UNHANDLED_TAC {instr}")
    return asm
