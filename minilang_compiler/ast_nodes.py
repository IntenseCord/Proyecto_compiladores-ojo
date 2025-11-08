"""AST node definitions for MiniLang."""
from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class Node:
    pass


@dataclass
class Program(Node):
    statements: List[Node]


@dataclass
class Read(Node):
    var: str


@dataclass
class Print(Node):
    expr: Any


@dataclass
class Assign(Node):
    target: str
    expr: Any


@dataclass
class If(Node):
    cond: Any
    then_block: List[Node]
    else_block: Optional[List[Node]] = None


@dataclass
class While(Node):
    cond: Any
    body: List[Node]


@dataclass
class BinaryOp(Node):
    op: str
    left: Any
    right: Any


@dataclass
class Literal(Node):
    value: int


@dataclass
class Var(Node):
    name: str
