"""Simple semantic tests: one valid program and one invalid (use-before-init)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import Parser
from minilang_compiler.semantic import SemanticAnalyzer, SemanticError


def test_good():
    sample = Path(__file__).parent / 'sample.minilang'
    text = sample.read_text(encoding='utf-8')
    tokens = tokenize(text)
    p = Parser(tokens)
    program = p.parse()
    sa = SemanticAnalyzer()
    sa.analyze(program)
    print('Semantic test OK — valid program analyzed successfully')


def test_bad():
    sample = Path(__file__).parent / 'bad.minilang'
    text = sample.read_text(encoding='utf-8')
    tokens = tokenize(text)
    p = Parser(tokens)
    program = p.parse()
    sa = SemanticAnalyzer()
    try:
        sa.analyze(program)
    except SemanticError as e:
        print('Semantic test OK — invalid program detected:', e)
        return
    print('Semantic test FAILED: expected error for use-before-init')
    sys.exit(2)


if __name__ == '__main__':
    test_good()
    test_bad()
