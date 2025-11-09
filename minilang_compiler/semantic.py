"""Analizador semántico para MiniLang.

Realiza comprobaciones básicas:
- Construye una tabla de símbolos (variables) y su estado de inicialización.
- Detecta uso de variables no inicializadas.
- Comprueba tipos (solo int implícito).
"""
from typing import Dict
from .ast_nodes import Program, FuncDef, Return, Read, Assign, Print, If, While, For, BinaryOp, UnaryOp, Literal, StringLiteral, Var, FuncCall


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        # symbol table: name -> initialized (bool)
        self.symbols: Dict[str, bool] = {}
        self.functions: Dict[str, int] = {}  # func_name -> param_count

    def analyze(self, program: Program):
        self.symbols = {}
        self.functions = {}
        # Analyze functions first
        for func in program.functions:
            if func.name in self.functions:
                raise SemanticError(f"Duplicate function definition: '{func.name}'")
            self.functions[func.name] = len(func.params)
            # Analyze function body with params initialized
            saved_symbols = self.symbols.copy()
            self.symbols = {param: True for param in func.params}
            for stmt in func.body:
                self.visit_stmt(stmt)
            self.symbols = saved_symbols
        # Analyze main program
        for stmt in program.statements:
            self.visit_stmt(stmt)
        return self.symbols

    def visit_stmt(self, node):
        if isinstance(node, Read):
            self.symbols[node.var] = True
            return
        if isinstance(node, Print):
            self.visit_expr(node.expr)
            return
        if isinstance(node, Return):
            self.visit_expr(node.expr)
            return
        if isinstance(node, Assign):
            self.visit_expr(node.expr)
            # assignment implicitly declares and initializes variable
            self.symbols[node.target] = True
            return
        if isinstance(node, If):
            self.visit_expr(node.cond)
            # analyze then-block
            for s in node.then_block:
                self.visit_stmt(s)
            # analyze else-block if present
            if node.else_block:
                for s in node.else_block:
                    self.visit_stmt(s)
            return
        if isinstance(node, While):
            self.visit_expr(node.cond)
            for s in node.body:
                self.visit_stmt(s)
            return
        if isinstance(node, For):
            # init
            self.visit_stmt(node.init)
            # condition
            self.visit_expr(node.cond)
            # update
            self.visit_expr(node.update.expr)
            # body
            for s in node.body:
                self.visit_stmt(s)
            return
        raise SemanticError(f"Unknown statement type: {type(node)}")

    def visit_expr(self, node):
        if isinstance(node, Literal):
            return
        if isinstance(node, StringLiteral):
            return
        if isinstance(node, Var):
            name = node.name
            if name not in self.symbols or not self.symbols[name]:
                raise SemanticError(f"Use of uninitialized variable '{name}'")
            return
        if isinstance(node, FuncCall):
            # Check function exists
            if node.name not in self.functions:
                raise SemanticError(f"Undefined function '{node.name}'")
            # Check argument count
            expected = self.functions[node.name]
            got = len(node.args)
            if expected != got:
                raise SemanticError(f"Function '{node.name}' expects {expected} arguments, got {got}")
            # Check arguments
            for arg in node.args:
                self.visit_expr(arg)
            return
        if isinstance(node, BinaryOp):
            self.visit_expr(node.left)
            self.visit_expr(node.right)
            return
        if isinstance(node, UnaryOp):
            self.visit_expr(node.operand)
            return
        raise SemanticError(f"Unknown expression type: {type(node)}")
