"""
test_parser.py: Verifica construcción de AST válido.
"""
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import Parser
from minilang_compiler import ast_nodes


def test_assignment():
    """Test parsing de asignación simple"""
    code = "x = 5; end;"
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    assert isinstance(program, ast_nodes.Program)
    assert len(program.statements) == 1
    assert isinstance(program.statements[0], ast_nodes.Assign)
    assert program.statements[0].target == "x"
    print("✓ test_assignment passed")


def test_arithmetic_expression():
    """Test parsing de expresiones aritméticas"""
    code = "x = 5 + 3 * 2; end;"
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    stmt = program.statements[0]
    assert isinstance(stmt, ast_nodes.Assign)
    assert isinstance(stmt.expr, ast_nodes.BinaryOp)
    assert stmt.expr.op == "+"
    print("✓ test_arithmetic_expression passed")


def test_if_statement():
    """Test parsing de if"""
    code = """
    if x > 5 {
        print x;
    }
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    assert isinstance(program.statements[0], ast_nodes.If)
    assert isinstance(program.statements[0].cond, ast_nodes.BinaryOp)
    assert len(program.statements[0].then_block) == 1
    print("✓ test_if_statement passed")


def test_if_elif_else():
    """Test parsing de if-elif-else"""
    code = """
    if x > 10 {
        print "A";
    } elif x > 5 {
        print "B";
    } else {
        print "C";
    }
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    if_stmt = program.statements[0]
    assert isinstance(if_stmt, ast_nodes.If)
    assert len(if_stmt.elif_blocks) == 1
    assert if_stmt.else_block is not None
    print("✓ test_if_elif_else passed")


def test_while_loop():
    """Test parsing de while"""
    code = """
    while x > 0 {
        x = x - 1;
    }
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    assert isinstance(program.statements[0], ast_nodes.While)
    assert len(program.statements[0].body) == 1
    print("✓ test_while_loop passed")


def test_for_loop():
    """Test parsing de for"""
    code = """
    for i = 0; i < 10; i = i + 1 {
        print i;
    }
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    assert isinstance(program.statements[0], ast_nodes.For)
    assert isinstance(program.statements[0].init, ast_nodes.Assign)
    assert isinstance(program.statements[0].cond, ast_nodes.BinaryOp)
    print("✓ test_for_loop passed")


def test_function_definition():
    """Test parsing de funciones"""
    code = """
    def suma(a, b) {
        return a + b;
    }
    x = 5;
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    assert len(program.functions) == 1
    assert program.functions[0].name == "suma"
    assert len(program.functions[0].params) == 2
    assert program.functions[0].params[0] == "a"
    print("✓ test_function_definition passed")


def test_function_call():
    """Test parsing de llamadas a funciones"""
    code = """
    def test() {
        return 1;
    }
    x = test();
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    assign = program.statements[0]
    assert isinstance(assign.expr, ast_nodes.FuncCall)
    assert assign.expr.name == "test"
    print("✓ test_function_call passed")


def test_logical_operators():
    """Test parsing de operadores lógicos"""
    code = """
    if x > 5 and y < 10 {
        print "yes";
    }
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    if_stmt = program.statements[0]
    assert isinstance(if_stmt.cond, ast_nodes.BinaryOp)
    assert if_stmt.cond.op == "and"
    print("✓ test_logical_operators passed")


def test_unary_operators():
    """Test parsing de operadores unarios"""
    code = """
    x = -5;
    y = not true;
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    assert isinstance(program.statements[0].expr, ast_nodes.UnaryOp)
    assert program.statements[0].expr.op == "-"
    assert isinstance(program.statements[1].expr, ast_nodes.UnaryOp)
    assert program.statements[1].expr.op == "not"
    print("✓ test_unary_operators passed")


def test_string_literals():
    """Test parsing de strings"""
    code = """
    print "Hello World";
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    print_stmt = program.statements[0]
    assert isinstance(print_stmt.expr, ast_nodes.StringLiteral)
    assert print_stmt.expr.value == "Hello World"
    print("✓ test_string_literals passed")


if __name__ == "__main__":
    print("Running Parser Tests...")
    test_assignment()
    test_arithmetic_expression()
    test_if_statement()
    test_if_elif_else()
    test_while_loop()
    test_for_loop()
    test_function_definition()
    test_function_call()
    test_logical_operators()
    test_unary_operators()
    test_string_literals()
    print("\n✅ All parser tests passed!")
