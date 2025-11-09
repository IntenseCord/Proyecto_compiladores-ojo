from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TokenType(Enum):
    # Special
    EOF = auto()
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()

    # Keywords
    READ = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    DEF = auto()
    RETURN = auto()
    END = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    ASSIGN = auto()

    # Relational
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    EQ = auto()
    NE = auto()

    # Separators
    SEMI = auto()
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()


@dataclass
class Token:
    type: TokenType
    value: Optional[str]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"
