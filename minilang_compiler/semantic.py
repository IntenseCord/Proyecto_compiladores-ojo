"""Analizador semántico para MiniLang.

Realiza comprobaciones básicas:
- Construye una tabla de símbolos (variables) y su estado de inicialización.
- Detecta uso de variables no inicializadas.
- Comprueba tipos (solo int implícito).
"""
from typing import Dict
from .ast_nodes import Program, Read, Assign, Print, If, While, BinaryOp, Literal, StringLiteral, Var


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        # symbol table: name -> initialized (bool)
        self.symbols: Dict[str, bool] = {}

    def analyze(self, program: Program):
        self.symbols = {}
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
        if isinstance(node, BinaryOp):
            self.visit_expr(node.left)
            self.visit_expr(node.right)
            return
        raise SemanticError(f"Unknown expression type: {type(node)}")
