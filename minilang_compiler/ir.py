"""Generador de código intermedio (TAC).

Genera instrucciones TAC desde el AST usando temporales t1, t2... y etiquetas L1, L2...
Instrucciones (op campo):
- 'label'        : a=label
- 'goto'         : a=label
- 'ifgoto'       : a=left, b=op, c=(right,label)  (represented as tuple in c)
- 'assign'       : a=target, b=source
- 'binop'        : a=target, b=op, c=(left,right)
- 'read'         : a=var
- 'print'        : a=expr
- 'param'        : a=expr (push parameter for function call)
- 'call'         : a=function_name, b=num_params, c=return_target (or None)
- 'return'       : a=expr (or None)
- 'func_start'   : a=function_name
- 'func_end'     : a=function_name
"""
from typing import List, Tuple, Any
from . import ast_nodes as ast


class TACInstr:
    def __init__(self, op: str, a: Any = None, b: Any = None, c: Any = None):
        self.op = op
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self) -> str:
        return f"TAC({self.op}, {self.a}, {self.b}, {self.c})"


class IRGenerator:
    def __init__(self):
        self.code: List[TACInstr] = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, instr: TACInstr):
        self.code.append(instr)

    def generate(self, program: ast.Program) -> List[TACInstr]:
        self.code = []
        self.functions = {}
        
        # If there are functions, generate a jump to main code
        if program.functions:
            main_label = self.new_label()
            self.emit(TACInstr('goto', a=main_label))
        
        # Generate code for all function definitions first
        for func in program.functions:
            self.functions[func.name] = func
            # func_start stores function name and parameter list
            self.emit(TACInstr('func_start', a=func.name, b=func.params))
            # Function parameters are already in scope (handled by VM)
            for stmt in func.body:
                self.gen_stmt(stmt)
            self.emit(TACInstr('func_end', a=func.name))
        
        # Then generate main program code
        if program.functions:
            self.emit(TACInstr('label', a=main_label))
        for stmt in program.statements:
            self.gen_stmt(stmt)
        return self.code

    def gen_stmt(self, node):
        if isinstance(node, ast.Read):
            self.emit(TACInstr('read', a=node.var))
            return
        if isinstance(node, ast.Print):
            v = self.gen_expr(node.expr)
            self.emit(TACInstr('print', a=v))
            return
        if isinstance(node, ast.Return):
            # For now, treat return like assignment to a special variable
            v = self.gen_expr(node.expr)
            self.emit(TACInstr('return', a=v))
            return
        if isinstance(node, ast.Assign):
            src = self.gen_expr(node.expr)
            self.emit(TACInstr('assign', a=node.target, b=src))
            return
        if isinstance(node, ast.If):
            # if-elif-else chain: generate labels for each branch
            end_label = self.new_label()
            
            # Generate code for initial if condition
            left, op, right = self.flatten_cond(node.cond)
            then_label = self.new_label()
            next_label = self.new_label()
            
            # if cond goto then_label else goto next_label
            self.emit(TACInstr('ifgoto', a=left, b=op, c=(right, then_label)))
            self.emit(TACInstr('goto', a=next_label))
            
            # then block
            self.emit(TACInstr('label', a=then_label))
            for s in node.then_block:
                self.gen_stmt(s)
            self.emit(TACInstr('goto', a=end_label))
            
            # elif blocks
            for elif_cond, elif_body in node.elif_blocks:
                self.emit(TACInstr('label', a=next_label))
                left, op, right = self.flatten_cond(elif_cond)
                elif_then_label = self.new_label()
                next_label = self.new_label()
                self.emit(TACInstr('ifgoto', a=left, b=op, c=(right, elif_then_label)))
                self.emit(TACInstr('goto', a=next_label))
                self.emit(TACInstr('label', a=elif_then_label))
                for s in elif_body:
                    self.gen_stmt(s)
                self.emit(TACInstr('goto', a=end_label))
            
            # else block
            self.emit(TACInstr('label', a=next_label))
            if node.else_block:
                for s in node.else_block:
                    self.gen_stmt(s)
            
            self.emit(TACInstr('label', a=end_label))
            return
        if isinstance(node, ast.While):
            start = self.new_label()
            body_label = self.new_label()
            end = self.new_label()
            self.emit(TACInstr('label', a=start))
            left, op, right = self.flatten_cond(node.cond)
            # if cond goto body_label
            self.emit(TACInstr('ifgoto', a=left, b=op, c=(right, body_label)))
            # else goto end
            self.emit(TACInstr('goto', a=end))
            self.emit(TACInstr('label', a=body_label))
            for s in node.body:
                self.gen_stmt(s)
            self.emit(TACInstr('goto', a=start))
            self.emit(TACInstr('label', a=end))
            return
        if isinstance(node, ast.For):
            # for init; cond; update { body }
            # Translate to: init; start: if cond goto body; goto end; body: ...; update; goto start; end:
            # Generate init
            self.gen_stmt(node.init)
            start = self.new_label()
            body_label = self.new_label()
            end = self.new_label()
            self.emit(TACInstr('label', a=start))
            left, op, right = self.flatten_cond(node.cond)
            # if cond goto body_label
            self.emit(TACInstr('ifgoto', a=left, b=op, c=(right, body_label)))
            # else goto end
            self.emit(TACInstr('goto', a=end))
            self.emit(TACInstr('label', a=body_label))
            # body
            for s in node.body:
                self.gen_stmt(s)
            # update
            self.gen_stmt(node.update)
            self.emit(TACInstr('goto', a=start))
            self.emit(TACInstr('label', a=end))
            return
        raise Exception(f"Unhandled stmt in IR generation: {node}")

    def flatten_cond(self, cond):
        # cond expected to be BinaryOp with relational operator
        if isinstance(cond, ast.BinaryOp) and cond.op in ('<', '>', '<=', '>=', '==', '!='):
            left = self.gen_expr(cond.left)
            right = self.gen_expr(cond.right)
            return left, cond.op, right
        # otherwise, evaluate expression and compare to 0
        temp = self.gen_expr(cond)
        return temp, '!=', '0'

    def gen_expr(self, node):
        if isinstance(node, ast.Literal):
            return str(node.value)
        if isinstance(node, ast.StringLiteral):
            # Return string with quotes to distinguish from variables
            return f'"{node.value}"'
        if isinstance(node, ast.Var):
            return node.name
        if isinstance(node, ast.FuncCall):
            # Generate PARAM instructions for each argument
            for arg in node.args:
                arg_val = self.gen_expr(arg)
                self.emit(TACInstr('param', a=arg_val))
            # Generate CALL instruction
            result = self.new_temp()
            self.emit(TACInstr('call', a=node.name, b=len(node.args), c=result))
            return result
        if isinstance(node, ast.UnaryOp):
            operand = self.gen_expr(node.operand)
            if node.op == '-':
                # Generate: t = 0 - operand
                t = self.new_temp()
                self.emit(TACInstr('binop', a=t, b='-', c=('0', operand)))
                return t
            elif node.op == '+':
                # Unary + is a no-op, just return operand
                return operand
            else:
                raise Exception(f"Unknown unary operator: {node.op}")
        if isinstance(node, ast.BinaryOp):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            t = self.new_temp()
            self.emit(TACInstr('binop', a=t, b=node.op, c=(left, right)))
            return t
        raise Exception(f"Unhandled expr in IR generation: {node}")
