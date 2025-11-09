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
    'MOD': 7,
    'JMP': 8,
    'JLT': 9,
    'JGT': 10,
    'JLE': 11,
    'JGE': 12,
    'JEQ': 13,
    'JNE': 14,
    'IN': 15,
    'OUT': 16,
    'PUSH': 17,
    'JZ': 18,
    'JNZ': 19,
    'LT': 20,
    'GT': 21,
    'LE': 22,
    'GE': 23,
    'EQ': 24,
    'NE': 25,
    'CALL': 26,
    'RET': 27,
    'PARAM': 28,
    'AND': 29,
    'OR': 30,
    'NOT': 31,
}


def assemble(asm_lines: List[str]):
    # Very simple assembler: translate mnemonics to opcode numbers, ignore labels
    machine = []
    for line in asm_lines:
        line = line.strip()
        if not line or line.startswith(';'):
            # Handle comments: store them as instructions so VM can process metadata
            if line.startswith('; PARAMS'):
                # Extract params metadata
                parts = line.split(None, 2)  # Split into [';', 'PARAMS', 'a,b,c']
                if len(parts) >= 3:
                    machine.append((';', ['PARAMS ' + parts[2]]))
            continue
        # Check if line contains a string literal (quoted text)
        if '"' in line:
            # Extract opcode and string literal separately
            first_quote = line.index('"')
            op_part = line[:first_quote].strip()
            string_part = line[first_quote:]
            parts = [op_part, string_part]
        else:
            parts = line.split()
        op = parts[0]
        opu = op.upper()
        # Labels end with ':'
        if opu.endswith(':'):
            # represent label as tuple ('label', name)
            machine.append(('label', opu[:-1]))
            continue
        # support PUSH, LOAD, STORE, ADD, SUB, MUL, DIV, JNZ, JZ, LT, GT, LE, GE, EQ, NE, IN, OUT, CALL, RET, PARAM
        code = OPCODES.get(opu)
        args = parts[1:]
        
        # Handle CALL specially to uppercase the function label
        if opu == 'CALL':
            call_args = [args[0].upper()] + args[1:]
            machine.append(('CALL', call_args))
            continue
            
        if code is None:
            # extend mapping for push and jumps
            if opu == 'PUSH':
                machine.append(('PUSH', args))
                continue
            if opu in ('JZ', 'JNZ'):
                machine.append((opu, args))
                continue
            if opu in ('LT','GT','LE','GE','EQ','NE','AND','OR','NOT'):
                machine.append((opu, args))
                continue
            if opu == 'RET':
                machine.append(('RET', args))
                continue
            if opu == 'PARAM':
                machine.append(('PARAM', args))
                continue
            # unknown -> store as raw
            machine.append((opu, args))
            continue
        # append mnemonic (string) rather than numeric opcode, VM expects strings
        machine.append((opu, args))
    return machine
