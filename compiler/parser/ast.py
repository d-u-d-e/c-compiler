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
    """An identifier is a string, but is not a string literal.
    It can be the name of a function or the name of a variable.
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
    """A function definition has a name identifier and a body.
    Currently arguments are not supported.
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
    """The program node is the root of the parse tree."""

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
    """A return statement is a statement."""

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
    """A constant node is an expression."""

    def __init__(self, parent: ASTNode | None, value):
        super().__init__(parent)
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self) -> str:
        return f"Constant({self._value})"
