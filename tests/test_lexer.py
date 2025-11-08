"""Simple test for the lexer. Run with plain Python.

This is not a pytest test; it's a small script that asserts expected token sequence
for the beginning of `tests/sample.minilang`.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from minilang_compiler.lexer import tokenize
from minilang_compiler.tokens import TokenType


def main():
    sample = Path(__file__).parent / 'sample.minilang'
    text = sample.read_text(encoding='utf-8')
    tokens = tokenize(text)
    # check the first statements: read a; read b;
    names = [t.type for t in tokens]
    expected_start = [TokenType.READ, TokenType.IDENT, TokenType.SEMI,
                      TokenType.READ, TokenType.IDENT, TokenType.SEMI]
    if names[:6] != expected_start:
        print('Lexer test FAILED')
        print('Got tokens:')
        for t in tokens[:12]:
            print(' ', t)
        sys.exit(2)
    print('Lexer test OK — first tokens as expected')


if __name__ == '__main__':
    main()
