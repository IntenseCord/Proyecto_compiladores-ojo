"""
test_full_pipeline.py: Tests end-to-end de compilación y ejecución.
"""
import sys
from pathlib import Path
from io import StringIO

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import Parser
from minilang_compiler.semantic import analyze
from minilang_compiler.ir import generate_ir
from minilang_compiler.optimizer import optimize
from minilang_compiler.codegen_machine import generate_machine_code
from minilang_compiler.runtime_vm import VirtualMachine


def compile_and_run(code):
    """Compila y ejecuta código MiniLang, retorna output capturado"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    program = parser.parse()
    analyze(program)
    ir = generate_ir(program)
    ir = optimize(ir)
    machine_code = generate_machine_code(ir)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = output = StringIO()
    
    try:
        vm = VirtualMachine(machine_code)
        vm.run()
        result = output.getvalue()
    finally:
        sys.stdout = old_stdout
    
    return result.strip()


def test_simple_arithmetic():
    """Test operaciones aritméticas básicas"""
    code = """
    x = 5 + 3;
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "8", f"Expected '8', got '{output}'"
    print("✓ test_simple_arithmetic passed")


def test_multiplication_precedence():
    """Test precedencia de operadores"""
    code = """
    x = 5 + 3 * 2;
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "11", f"Expected '11', got '{output}'"
    print("✓ test_multiplication_precedence passed")


def test_if_statement():
    """Test condicional if"""
    code = """
    x = 10;
    if x > 5 {
        print "yes";
    }
    end;
    """
    output = compile_and_run(code)
    assert output == "yes", f"Expected 'yes', got '{output}'"
    print("✓ test_if_statement passed")


def test_if_else():
    """Test condicional if-else"""
    code = """
    x = 3;
    if x > 5 {
        print "big";
    } else {
        print "small";
    }
    end;
    """
    output = compile_and_run(code)
    assert output == "small", f"Expected 'small', got '{output}'"
    print("✓ test_if_else passed")


def test_elif_chain():
    """Test cadena elif"""
    code = """
    x = 7;
    if x > 10 {
        print "A";
    } elif x > 5 {
        print "B";
    } else {
        print "C";
    }
    end;
    """
    output = compile_and_run(code)
    assert output == "B", f"Expected 'B', got '{output}'"
    print("✓ test_elif_chain passed")


def test_while_loop():
    """Test loop while"""
    code = """
    x = 0;
    while x < 3 {
        print x;
        x = x + 1;
    }
    end;
    """
    output = compile_and_run(code)
    expected = "0\n1\n2"
    assert output == expected, f"Expected '{expected}', got '{output}'"
    print("✓ test_while_loop passed")


def test_for_loop():
    """Test loop for"""
    code = """
    for i = 1; i <= 3; i = i + 1 {
        print i;
    }
    end;
    """
    output = compile_and_run(code)
    expected = "1\n2\n3"
    assert output == expected, f"Expected '{expected}', got '{output}'"
    print("✓ test_for_loop passed")


def test_function_simple():
    """Test función simple"""
    code = """
    def test() {
        return 42;
    }
    x = test();
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "42", f"Expected '42', got '{output}'"
    print("✓ test_function_simple passed")


def test_function_with_params():
    """Test función con parámetros"""
    code = """
    def suma(a, b) {
        return a + b;
    }
    x = suma(5, 10);
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "15", f"Expected '15', got '{output}'"
    print("✓ test_function_with_params passed")


def test_logical_and():
    """Test operador AND"""
    code = """
    x = 10;
    y = 5;
    if x > 5 and y < 10 {
        print "yes";
    }
    end;
    """
    output = compile_and_run(code)
    assert output == "yes", f"Expected 'yes', got '{output}'"
    print("✓ test_logical_and passed")


def test_logical_or():
    """Test operador OR"""
    code = """
    x = 3;
    if x > 10 or x < 5 {
        print "yes";
    }
    end;
    """
    output = compile_and_run(code)
    assert output == "yes", f"Expected 'yes', got '{output}'"
    print("✓ test_logical_or passed")


def test_logical_not():
    """Test operador NOT"""
    code = """
    x = 0;
    if not x {
        print "yes";
    }
    end;
    """
    output = compile_and_run(code)
    assert output == "yes", f"Expected 'yes', got '{output}'"
    print("✓ test_logical_not passed")


def test_modulo_operator():
    """Test operador módulo"""
    code = """
    x = 10 % 3;
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "1", f"Expected '1', got '{output}'"
    print("✓ test_modulo_operator passed")


def test_unary_minus():
    """Test operador unario menos"""
    code = """
    x = -5;
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "-5", f"Expected '-5', got '{output}'"
    print("✓ test_unary_minus passed")


def test_string_output():
    """Test salida de strings"""
    code = """
    print "Hello World";
    end;
    """
    output = compile_and_run(code)
    assert output == "Hello World", f"Expected 'Hello World', got '{output}'"
    print("✓ test_string_output passed")


def test_complex_expression():
    """Test expresión compleja"""
    code = """
    x = (10 + 5) * 2 - 8 / 4;
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "28", f"Expected '28', got '{output}'"
    print("✓ test_complex_expression passed")


def test_nested_function_calls():
    """Test llamadas anidadas"""
    code = """
    def doble(n) {
        return n * 2;
    }
    def suma(a, b) {
        return a + b;
    }
    x = suma(doble(3), 4);
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "10", f"Expected '10', got '{output}'"
    print("✓ test_nested_function_calls passed")


def test_recursive_factorial():
    """Test recursión simple"""
    code = """
    def factorial(n) {
        if n <= 1 {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    x = factorial(5);
    print x;
    end;
    """
    output = compile_and_run(code)
    assert output == "120", f"Expected '120', got '{output}'"
    print("✓ test_recursive_factorial passed")


if __name__ == "__main__":
    print("Running Full Pipeline Tests...")
    test_simple_arithmetic()
    test_multiplication_precedence()
    test_if_statement()
    test_if_else()
    test_elif_chain()
    test_while_loop()
    test_for_loop()
    test_function_simple()
    test_function_with_params()
    test_logical_and()
    test_logical_or()
    test_logical_not()
    test_modulo_operator()
    test_unary_minus()
    test_string_output()
    test_complex_expression()
    test_nested_function_calls()
    test_recursive_factorial()
    print("\n✅ All full pipeline tests passed!")
