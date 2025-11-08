"""Script orquestador para el pipeline del compilador (fase inicial).

Actualmente ejecuta: fuente -> tokens
Próximos pasos: parser -> semántica -> IR -> ASM -> máquina -> VM
"""
import argparse
from pathlib import Path
import sys
import os

# If this script is run directly (python minilang_compiler/compiler.py), ensure
# the project root is on sys.path so absolute imports like
# `from minilang_compiler.lexer import tokenize` work.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from minilang_compiler.lexer import tokenize


def main():
    parser = argparse.ArgumentParser(description="MiniLang compiler (early stage)")
    parser.add_argument("source", nargs="?", help="MiniLang source file", default=str(Path(__file__).parent.parent / "tests" / "sample.minilang"))
    parser.add_argument("--run", action="store_true", help="Run resulting VM after compilation")
    args = parser.parse_args()
    src_path = Path(args.source)
    if not src_path.exists():
        print(f"Source file not found: {src_path}")
        return

    text = src_path.read_text(encoding='utf-8')
    try:
        tokens = tokenize(text)
        print("Tokens:")
        for t in tokens:
            print("  ", t)
    except Exception as e:
        print("Lexing error:", e)
        return

    # parse
    from minilang_compiler.parser import Parser
    from minilang_compiler.semantic import SemanticAnalyzer
    from minilang_compiler.ir import IRGenerator
    from minilang_compiler.optimizer import constant_folding
    from minilang_compiler.codegen_asm import generate_asm
    from minilang_compiler.codegen_machine import assemble
    from minilang_compiler.runtime_vm import SimpleVM

    try:
        p = Parser(tokens)
        program = p.parse()
    except Exception as e:
        print('Parser error:', e)
        return

    try:
        sa = SemanticAnalyzer()
        sa.analyze(program)
    except Exception as e:
        print('Semantic error:', e)
        return

    # IR
    irgen = IRGenerator()
    tac = irgen.generate(program)
    print('\nTAC:')
    for i in tac:
        print('  ', i)

    # optimize
    tac_opt = constant_folding(tac)

    asm = generate_asm(tac_opt)
    print('\nAssembly:')
    for line in asm:
        print('  ', line)

    machine = assemble(asm)
    print('\nMachine (assembled):')
    for instr in machine:
        print('  ', instr)

    if args.run:
        print('\n--- Running VM ---')
        vm = SimpleVM(machine)
        vm.run()


if __name__ == '__main__':
    main()
