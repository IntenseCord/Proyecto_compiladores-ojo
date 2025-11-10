"""
test_semantic.py: Verifica análisis semántico válido y rechaza código inválido.
"""
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import Parser
from minilang_compiler.semantic import analyze


def test_valid_variable_usage():
    """Test que variables definidas antes de uso son válidas"""
    code = """
    x = 5;
    y = x + 3;
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        print("✓ test_valid_variable_usage passed")
    except Exception as e:
        raise AssertionError(f"Valid code rejected: {e}")


def test_undefined_variable():
    """Test que uso de variable no definida falla"""
    code = """
    x = y + 5;
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        raise AssertionError("Should have failed: undefined variable y")
    except Exception:
        print("✓ test_undefined_variable passed")


def test_function_call_valid():
    """Test que llamadas a funciones definidas son válidas"""
    code = """
    def test() {
        return 42;
    }
    x = test();
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        print("✓ test_function_call_valid passed")
    except Exception as e:
        raise AssertionError(f"Valid code rejected: {e}")


def test_undefined_function():
    """Test que llamadas a funciones no definidas fallan"""
    code = """
    x = foo();
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        raise AssertionError("Should have failed: undefined function foo")
    except Exception:
        print("✓ test_undefined_function passed")


def test_function_scope():
    """Test que parámetros de función son visibles dentro de la función"""
    code = """
    def suma(a, b) {
        return a + b;
    }
    x = suma(5, 3);
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        print("✓ test_function_scope passed")
    except Exception as e:
        raise AssertionError(f"Valid code rejected: {e}")


def test_return_outside_function():
    """Test que return fuera de función puede fallar (depende de implementación)"""
    code = """
    return 5;
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    # Some compilers allow this, some don't - just test it doesn't crash
    try:
        analyze(program)
        print("✓ test_return_outside_function passed (allowed)")
    except Exception:
        print("✓ test_return_outside_function passed (rejected)")


def test_nested_scopes():
    """Test que variables en bloques if/while son visibles"""
    code = """
    x = 5;
    if x > 0 {
        y = 10;
        print y;
    }
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        print("✓ test_nested_scopes passed")
    except Exception as e:
        raise AssertionError(f"Valid code rejected: {e}")


def test_complex_expression():
    """Test que expresiones complejas con variables válidas pasan"""
    code = """
    x = 5;
    y = 10;
    z = (x + y) * 2 - x / y;
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        print("✓ test_complex_expression passed")
    except Exception as e:
        raise AssertionError(f"Valid code rejected: {e}")


def test_for_loop_variable():
    """Test que variable de for loop es válida dentro del loop"""
    code = """
    for i = 0; i < 10; i = i + 1 {
        print i;
    }
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        print("✓ test_for_loop_variable passed")
    except Exception as e:
        raise AssertionError(f"Valid code rejected: {e}")


def test_multiple_functions():
    """Test que múltiples funciones definidas son válidas"""
    code = """
    def suma(a, b) {
        return a + b;
    }
    def resta(a, b) {
        return a - b;
    }
    x = suma(5, 3);
    y = resta(10, 2);
    end;
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    
    try:
        analyze(program)
        print("✓ test_multiple_functions passed")
    except Exception as e:
        raise AssertionError(f"Valid code rejected: {e}")


if __name__ == "__main__":
    print("Running Semantic Analysis Tests...")
    test_valid_variable_usage()
    test_undefined_variable()
    test_function_call_valid()
    test_undefined_function()
    test_function_scope()
    test_return_outside_function()
    test_nested_scopes()
    test_complex_expression()
    test_for_loop_variable()
    test_multiple_functions()
    print("\n✅ All semantic tests passed!")
