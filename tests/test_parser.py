"""Simple parser test: tokenize sample and parse into AST."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import Parser
import minilang_compiler.ast_nodes as ast


def main():
    sample = Path(__file__).parent / 'sample.minilang'
    text = sample.read_text(encoding='utf-8')
    tokens = tokenize(text)
    p = Parser(tokens)
    program = p.parse()
    # basic checks
    if not isinstance(program, ast.Program):
        print('Parser test FAILED: root is not Program')
        sys.exit(2)

    # look for an If and a While in top-level statements
    found_if = any(isinstance(s, ast.If) for s in program.statements)
    found_while = any(isinstance(s, ast.While) for s in program.statements)
    if not (found_if and found_while):
        print('Parser test FAILED: expected If and While in program statements')
        print('Statements:', program.statements)
        sys.exit(2)

    print('Parser test OK — AST structure as expected')


if __name__ == '__main__':
    main()
