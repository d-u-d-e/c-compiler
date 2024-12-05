from abc import abstractmethod

from lib.ast.ast import ASTNode


class Exp(ASTNode):
    """Abstract class denoting a generic expression."""

    @abstractmethod
    def __init__(self, parent: ASTNode | None, **kwargs):
        super().__init__(parent, **kwargs)


class Statement(ASTNode):
    """Abstract class denoting a generic statement."""

    @abstractmethod
    def __init__(self, parent: ASTNode | None, **kwargs):
        super().__init__(parent, **kwargs)


class Identifier(ASTNode):
    """
    Represents an identifier in the abstract syntax tree (AST).

    An identifier is a named reference that is not a string literal. It can be used
    to represent the name of a function, a variable, or other symbolic elements in
    the program.
    """

    def __init__(self, parent: ASTNode | None, value: str):
        super().__init__(parent)
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self) -> str:
        return f"Identifier({self._value})"


class Function(ASTNode):
    """Represents a function definition in the abstract syntax tree (AST).

    A function definition consists of a name (identifier) and a body (statement).
    Currently, this class does not support function arguments.
    """

    def __init__(self, parent: ASTNode | None, name: Identifier, body: Statement):
        super().__init__(parent)
        name.parent = self
        body.parent = self
        self._name = name
        self._body = body
        # Used by get_node_repr to prefix the representation of each child with
        # "name=...", "body=..."
        name.field_name = "name"
        body.field_name = "body"

    @property
    def name(self) -> Identifier:
        return self._name

    @property
    def body(self) -> Statement:
        return self._body

    def __repr__(self) -> str:
        return "Function"


class Program(ASTNode):
    """Represents the root node of the parse tree."""

    def __init__(self, func_def: Function):
        super().__init__()
        self._func_def = func_def
        func_def.parent = self

    @property
    def function_definition(self) -> Function:
        return self._func_def

    def __repr__(self) -> str:
        return "Program"


class Return(Statement):
    """Represents a return statement in the abstract syntax tree (AST)."""

    def __init__(self, parent: ASTNode | None, exp: Exp):
        super().__init__(parent)
        self._exp = exp
        exp.parent = self

    @property
    def exp(self) -> Exp:
        return self._exp

    def __repr__(self) -> str:
        return "Return"


class Constant(Exp):
    """Represents a constant value in the abstract syntax tree (AST).

    A constant node is an expression that holds a fixed value, such as an integer,
    floating-point number, or string literal.
    """

    def __init__(self, parent: ASTNode | None, value):
        super().__init__(parent)
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self) -> str:
        return f"Constant({self._value})"
