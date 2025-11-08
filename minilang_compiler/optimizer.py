"""Optimizaciones sobre el TAC (opcional).

Se pueden implementar optimizaciones como constant folding y dead code elimination.
"""
from .ir import TACInstr


def constant_folding(tac_list):
    new_list = []
    for instr in tac_list:
        if instr.op == 'binop':
            target = instr.a
            op = instr.b
            left, right = instr.c
            # both constants?
            try:
                lval = int(left)
                rval = int(right)
                if op == '+':
                    val = lval + rval
                elif op == '-':
                    val = lval - rval
                elif op == '*':
                    val = lval * rval
                elif op == '/':
                    val = lval // rval if rval != 0 else 0
                else:
                    # relational or others: keep as is
                    new_list.append(instr)
                    continue
                # replace with assign target = const
                new_list.append(TACInstr('assign', a=target, b=str(val)))
                continue
            except ValueError:
                # non-constant, keep
                new_list.append(instr)
                continue
        else:
            new_list.append(instr)
    return new_list
