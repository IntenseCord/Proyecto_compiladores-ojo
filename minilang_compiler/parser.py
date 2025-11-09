"""Parser recursivo descendente para MiniLang.

Construye el AST definido en `ast_nodes.py`.
"""
from typing import List
from .tokens import Token, TokenType
from . import ast_nodes


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = Token(TokenType.EOF, None, -1, -1)

    def expect(self, ttype: TokenType):
        if self.current.type == ttype:
            tok = self.current
            self.advance()
            return tok
        raise ParserError(f"Expected {ttype.name} at {self.current.line}:{self.current.column}, got {self.current.type.name}")

    def parse(self) -> ast_nodes.Program:
        stmts = []
        while self.current.type != TokenType.END and self.current.type != TokenType.EOF:
            stmts.append(self.parse_stmt())
        # consume 'end'
        if self.current.type == TokenType.END:
            self.advance()
        else:
            raise ParserError(f"Expected 'end' at {self.current.line}:{self.current.column}")
        # optional EOF
        return ast_nodes.Program(statements=stmts)

    def parse_stmt(self):
        ct = self.current.type
        if ct == TokenType.READ:
            self.advance()
            ident = self.expect(TokenType.IDENT)
            self.expect(TokenType.SEMI)
            return ast_nodes.Read(var=ident.value)

        if ct == TokenType.PRINT:
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.SEMI)
            return ast_nodes.Print(expr=expr)

        if ct == TokenType.IDENT:
            ident = self.current
            self.advance()
            # assignment
            if self.current.type == TokenType.ASSIGN:
                self.advance()
                expr = self.parse_expr()
                self.expect(TokenType.SEMI)
                return ast_nodes.Assign(target=ident.value, expr=expr)
            else:
                raise ParserError(f"Unexpected token after identifier at {self.current.line}:{self.current.column}")

        if ct == TokenType.IF:
            self.advance()
            cond = self.parse_expr()
            self.expect(TokenType.LBRACE)
            then_block = self.parse_block()
            else_block = None
            if self.current.type == TokenType.ELSE:
                self.advance()
                self.expect(TokenType.LBRACE)
                else_block = self.parse_block()
            return ast_nodes.If(cond=cond, then_block=then_block, else_block=else_block)

        if ct == TokenType.WHILE:
            self.advance()
            cond = self.parse_expr()
            self.expect(TokenType.LBRACE)
            body = self.parse_block()
            return ast_nodes.While(cond=cond, body=body)

        raise ParserError(f"Unexpected token {self.current.type.name} at {self.current.line}:{self.current.column}")

    def parse_block(self):
        stmts = []
        while self.current.type != TokenType.RBRACE and self.current.type != TokenType.EOF:
            stmts.append(self.parse_stmt())
        self.expect(TokenType.RBRACE)
        return stmts

    # Expressions: support relational operators and arithmetic with precedence
    def parse_expr(self):
        left = self.parse_additive()
        # relational operators
        if self.current.type in (TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE, TokenType.EQ, TokenType.NE):
            op_token = self.current
            self.advance()
            right = self.parse_additive()
            return ast_nodes.BinaryOp(op=op_token.value, left=left, right=right)
        return left

    def parse_additive(self):
        node = self.parse_term()
        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current.value
            self.advance()
            right = self.parse_term()
            node = ast_nodes.BinaryOp(op=op, left=node, right=right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current.type in (TokenType.MUL, TokenType.DIV):
            op = self.current.value
            self.advance()
            right = self.parse_factor()
            node = ast_nodes.BinaryOp(op=op, left=node, right=right)
        return node

    def parse_factor(self):
        ct = self.current.type
        if ct == TokenType.NUMBER:
            val = int(self.current.value)
            self.advance()
            return ast_nodes.Literal(value=val)
        if ct == TokenType.STRING:
            val = self.current.value
            self.advance()
            return ast_nodes.StringLiteral(value=val)
        if ct == TokenType.IDENT:
            name = self.current.value
            self.advance()
            return ast_nodes.Var(name=name)
        if ct == TokenType.LPAREN:
            # consume '('
            self.advance()
            node = self.parse_expr()
            # expect ')'
            if self.current.type != TokenType.RPAREN:
                raise ParserError(f"Expected ')' at {self.current.line}:{self.current.column}")
            self.advance()
            return node

        raise ParserError(f"Unexpected factor {self.current.type.name} ({self.current.value}) at {self.current.line}:{self.current.column}")
