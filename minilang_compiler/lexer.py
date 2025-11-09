"""Analizador léxico para MiniLang.

Proporciona la clase `Lexer` que convierte texto fuente en una lista de `Token`.
"""
from typing import List
from .tokens import Token, TokenType


class LexerError(Exception):
    pass


KEYWORDS = {
    "read": TokenType.READ,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "def": TokenType.DEF,
    "return": TokenType.RETURN,
    "end": TokenType.END,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
}


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.current = text[0] if text else ""

    def advance(self):
        if self.current == "\n":
            self.line += 1
            self.col = 0
        self.pos += 1
        if self.pos >= len(self.text):
            self.current = ""
        else:
            self.current = self.text[self.pos]
        self.col += 1

    def peek(self):
        nxt = self.pos + 1
        if nxt >= len(self.text):
            return ""
        return self.text[nxt]

    def skip_whitespace_and_comments(self):
        """Skip spaces, newlines and comments (// single-line and /* ... */ block).

        Raises LexerError on unterminated block comments.
        """
        while True:
            if not self.current:
                return
            # whitespace
            if self.current.isspace():
                self.advance()
                continue

            # single-line comment //
            if self.current == '/' and self.peek() == '/':
                while self.current and self.current != '\n':
                    self.advance()
                continue

            # block comment /* ... */
            if self.current == '/' and self.peek() == '*':
                # consume '/*'
                self.advance(); self.advance()
                while self.current and not (self.current == '*' and self.peek() == '/'):
                    self.advance()
                if self.current == '*' and self.peek() == '/':
                    self.advance(); self.advance()
                    continue
                raise LexerError(f"Unterminated block comment at {self.line}:{self.col}")

            break

    def make_number(self):
        start_col = self.col
        num_str = ''
        while self.current and self.current.isdigit():
            num_str += self.current
            self.advance()
        return Token(TokenType.NUMBER, num_str, self.line, start_col)

    def make_ident_or_keyword(self):
        start_col = self.col
        s = ''
        while self.current and (self.current.isalnum() or self.current == '_'):
            s += self.current
            self.advance()
        typ = KEYWORDS.get(s, TokenType.IDENT)
        return Token(typ, s, self.line, start_col)

    def make_string(self):
        """Parse a string literal enclosed in double quotes."""
        start_col = self.col
        self.advance()  # skip opening "
        s = ''
        while self.current and self.current != '"':
            if self.current == '\\' and self.peek() == '"':
                # Handle escaped quote
                s += '"'
                self.advance()
                self.advance()
            elif self.current == '\\' and self.peek() == 'n':
                # Handle newline escape
                s += '\n'
                self.advance()
                self.advance()
            elif self.current == '\\' and self.peek() == '\\':
                # Handle escaped backslash
                s += '\\'
                self.advance()
                self.advance()
            else:
                s += self.current
                self.advance()
        if self.current != '"':
            raise LexerError(f"Unterminated string at {self.line}:{start_col}")
        self.advance()  # skip closing "
        return Token(TokenType.STRING, s, self.line, start_col)

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.current:
            if self.current.isspace() or self.current == '/':
                self.skip_whitespace_and_comments()
                continue

            if self.current.isalpha() or self.current == '_':
                tokens.append(self.make_ident_or_keyword())
                continue

            if self.current.isdigit():
                tokens.append(self.make_number())
                continue

            # string literal
            if self.current == '"':
                tokens.append(self.make_string())
                continue

            # two-char operators
            if self.current == '<' and self.peek() == '=':
                tokens.append(Token(TokenType.LE, '<=', self.line, self.col))
                self.advance(); self.advance();
                continue
            if self.current == '>' and self.peek() == '=':
                tokens.append(Token(TokenType.GE, '>=', self.line, self.col))
                self.advance(); self.advance();
                continue
            if self.current == '=' and self.peek() == '=':
                tokens.append(Token(TokenType.EQ, '==', self.line, self.col))
                self.advance(); self.advance();
                continue
            if self.current == '!' and self.peek() == '=':
                tokens.append(Token(TokenType.NE, '!=', self.line, self.col))
                self.advance(); self.advance();
                continue

            # single-char tokens
            ch = self.current
            if ch == '+':
                tokens.append(Token(TokenType.PLUS, ch, self.line, self.col))
            elif ch == '-':
                tokens.append(Token(TokenType.MINUS, ch, self.line, self.col))
            elif ch == '*':
                tokens.append(Token(TokenType.MUL, ch, self.line, self.col))
            elif ch == '/':
                tokens.append(Token(TokenType.DIV, ch, self.line, self.col))
            elif ch == '%':
                tokens.append(Token(TokenType.MOD, ch, self.line, self.col))
            elif ch == '=':
                tokens.append(Token(TokenType.ASSIGN, ch, self.line, self.col))
            elif ch == '<':
                tokens.append(Token(TokenType.LT, ch, self.line, self.col))
            elif ch == '>':
                tokens.append(Token(TokenType.GT, ch, self.line, self.col))
            elif ch == ';':
                tokens.append(Token(TokenType.SEMI, ch, self.line, self.col))
            elif ch == '{':
                tokens.append(Token(TokenType.LBRACE, ch, self.line, self.col))
            elif ch == '}':
                tokens.append(Token(TokenType.RBRACE, ch, self.line, self.col))
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, ch, self.line, self.col))
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ch, self.line, self.col))
            elif ch == ',':
                tokens.append(Token(TokenType.COMMA, ch, self.line, self.col))
            else:
                raise LexerError(f"Unexpected character {ch!r} at {self.line}:{self.col}")

            self.advance()

        tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return tokens


def tokenize(text: str):
    l = Lexer(text)
    return l.tokenize()
