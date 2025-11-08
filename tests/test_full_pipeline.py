"""Test full pipeline: compile and run a small program without input.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import Parser
from minilang_compiler.semantic import SemanticAnalyzer
from minilang_compiler.ir import IRGenerator
from minilang_compiler.optimizer import constant_folding
from minilang_compiler.codegen_asm import generate_asm
from minilang_compiler.codegen_machine import assemble
from minilang_compiler.runtime_vm import SimpleVM


def main():
    sample = Path(__file__).parent / 'simple_noio.minilang'
    text = sample.read_text(encoding='utf-8')
    tokens = tokenize(text)
    p = Parser(tokens)
    program = p.parse()
    sa = SemanticAnalyzer()
    sa.analyze(program)
    irgen = IRGenerator()
    tac = irgen.generate(program)
    tac_opt = constant_folding(tac)
    asm = generate_asm(tac_opt)
    machine = assemble(asm)
    vm = SimpleVM(machine)
    # capture stdout of vm.run()
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        vm.run()
    out = buf.getvalue().strip()
    # expected output is the computed sum: i=2, j=3, sum = 2 + 3*4 = 14
    if '14' in out:
        print('Full pipeline test OK — output contains 14')
    else:
        print('Full pipeline test FAILED — output was:\n', out)
        sys.exit(2)


if __name__ == '__main__':
    main()
