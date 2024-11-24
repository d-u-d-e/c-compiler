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


class Program(ASTNode):
    """The program node is the root of the parse tree."""

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return "Program"


class Identifier(ASTNode):
    """An identifier is a string, but is not a string literal.
    It can be the name of a function or the name of a variable.
    """

    def __init__(self, parent: ASTNode | None, name: str):
        super().__init__(parent)
        self.name = name

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


class FunctionDefinition(ASTNode):
    """A function definition has a name identifier and a body.
    Currently arguments are not supported.
    """

    def __init__(
        self, parent: ASTNode | None, identifier: Identifier, statement: Statement
    ):
        super().__init__(parent)
        identifier.parent = self
        statement.parent = self
        self._name = identifier
        self._body = statement
        # used by get_node_repr to prefix the representation of each child with
        # "name=...", "body=..."
        identifier.field_name = "name"
        statement.field_name = "body"

    @property
    def name(self) -> Identifier:
        return self._name

    @property
    def body(self):
        return self._body

    def __repr__(self) -> str:
        return "FunctionDefinition"


class Return(Statement):
    """A return statement is a statement."""

    def __init__(self, parent: ASTNode | None):
        super().__init__(parent)

    def __repr__(self) -> str:
        return "Return"


class Constant(Exp):
    """A constant node is an expression."""

    def __init__(self, parent: ASTNode | None, value):
        super().__init__(parent)
        self.value = value

    def __repr__(self) -> str:
        return f"Constant({self.value})"
