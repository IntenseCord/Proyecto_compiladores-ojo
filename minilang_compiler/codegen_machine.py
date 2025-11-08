"""Generador de código máquina (opcodes numéricos) desde ensamblador simbólico."""
from typing import List


OPCODES = {
    # sample mapping
    'LOAD': 1,
    'STORE': 2,
    'ADD': 3,
    'SUB': 4,
    'MUL': 5,
    'DIV': 6,
    'JMP': 7,
    'JLT': 8,
    'JGT': 9,
    'JLE': 10,
    'JGE': 11,
    'JEQ': 12,
    'JNE': 13,
    'IN': 14,
    'OUT': 15,
    'PUSH': 16,
    'JZ': 17,
    'JNZ': 18,
    'LT': 19,
    'GT': 20,
    'LE': 21,
    'GE': 22,
    'EQ': 23,
    'NE': 24,
}


def assemble(asm_lines: List[str]):
    # Very simple assembler: translate mnemonics to opcode numbers, ignore labels
    machine = []
    for line in asm_lines:
        line = line.strip()
        if not line or line.startswith(';'):
            continue
        parts = line.split()
        op = parts[0]
        opu = op.upper()
        # Labels end with ':'
        if opu.endswith(':'):
            # represent label as tuple ('label', name)
            machine.append(('label', opu[:-1]))
            continue
        # support PUSH, LOAD, STORE, ADD, SUB, MUL, DIV, JNZ, JZ, LT, GT, LE, GE, EQ, NE, IN, OUT
        code = OPCODES.get(opu)
        args = parts[1:]
        if code is None:
            # extend mapping for push and jumps
            if opu == 'PUSH':
                machine.append(('PUSH', args))
                continue
            if opu in ('JZ', 'JNZ'):
                machine.append((opu, args))
                continue
            if opu in ('LT','GT','LE','GE','EQ','NE'):
                machine.append((opu, args))
                continue
            # unknown -> store as raw
            machine.append((opu, args))
            continue
        # append mnemonic (string) rather than numeric opcode, VM expects strings
        machine.append((opu, args))
    return machine
