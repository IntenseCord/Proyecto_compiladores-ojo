"""
test_lexer.py: Verifica tokenización correcta.
"""
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from minilang_compiler.lexer import tokenize
from minilang_compiler.tokens import TokenType


def test_basic_tokens():
    """Test tokenización de operadores básicos"""
    code = "x = 5 + 3;"
    tokens = tokenize(code)
    
    assert tokens[0].type == TokenType.IDENT
    assert tokens[0].value == "x"
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == "5"
    assert tokens[3].type == TokenType.PLUS
    assert tokens[4].type == TokenType.NUMBER
    assert tokens[5].type == TokenType.SEMI
    print("✓ test_basic_tokens passed")


def test_keywords():
    """Test tokenización de palabras clave"""
    code = "if while for def return end"
    tokens = tokenize(code)
    
    assert tokens[0].type == TokenType.IF
    assert tokens[1].type == TokenType.WHILE
    assert tokens[2].type == TokenType.FOR
    assert tokens[3].type == TokenType.DEF
    assert tokens[4].type == TokenType.RETURN
    assert tokens[5].type == TokenType.END
    print("✓ test_keywords passed")


def test_strings():
    """Test tokenización de strings"""
    code = 'print "Hello World";'
    tokens = tokenize(code)
    
    assert tokens[0].type == TokenType.PRINT
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "Hello World"
    assert tokens[2].type == TokenType.SEMI
    print("✓ test_strings passed")


def test_operators():
    """Test todos los operadores"""
    code = "+ - * / % < > <= >= == != and or not"
    tokens = tokenize(code)
    
    assert tokens[0].type == TokenType.PLUS
    assert tokens[1].type == TokenType.MINUS
    assert tokens[2].type == TokenType.MUL
    assert tokens[3].type == TokenType.DIV
    assert tokens[4].type == TokenType.MOD
    assert tokens[5].type == TokenType.LT
    assert tokens[6].type == TokenType.GT
    assert tokens[7].type == TokenType.LE
    assert tokens[8].type == TokenType.GE
    assert tokens[9].type == TokenType.EQ
    assert tokens[10].type == TokenType.NE
    assert tokens[11].type == TokenType.AND
    assert tokens[12].type == TokenType.OR
    assert tokens[13].type == TokenType.NOT
    print("✓ test_operators passed")


def test_comments_and_whitespace():
    """Test manejo de espacios y saltos de línea"""
    code = """x = 5
    y = 10
    """
    tokens = tokenize(code)
    
    # Should have: x, =, 5, y, =, 10, EOF
    assert tokens[0].type == TokenType.IDENT
    assert tokens[0].value == "x"
    assert tokens[3].type == TokenType.IDENT
    assert tokens[3].value == "y"
    print("✓ test_comments_and_whitespace passed")


def test_relational_operators():
    """Test operadores relacionales"""
    code = "x <= y; a >= b; c == d; e != f;"
    tokens = tokenize(code)
    
    assert tokens[1].type == TokenType.LE
    assert tokens[5].type == TokenType.GE
    assert tokens[9].type == TokenType.EQ
    assert tokens[13].type == TokenType.NE
    print("✓ test_relational_operators passed")


if __name__ == "__main__":
    print("Running Lexer Tests...")
    test_basic_tokens()
    test_keywords()
    test_strings()
    test_operators()
    test_comments_and_whitespace()
    test_relational_operators()
    print("\n✅ All lexer tests passed!")
