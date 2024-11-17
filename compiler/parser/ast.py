from abc import abstractmethod
from typing import Optional

from lib.tree.node import TreeNode
from lib.tree.tree import Tree


class ASTNode(TreeNode):
    """Abstract class denoting a generic AST node.

    All nodes shares the `get_node_repr` method to obtain a pretty
    representation rooted at `self`.
    """

    @abstractmethod
    def __init__(self, parent: Optional["ASTNode"] = None, **kwargs):
        super().__init__(parent, **kwargs)

    def get_node_repr(self, level: int, fill: str, pre: str = "", end: str = "") -> str:
        """Gets the subtree representation rooted at `self`.

        Args:
            level: Integer representing the level of the subtree at this node.
            fill: Indicates which string to use as a filler to make the representation look pretty.
            pre: Prefix string inserted after the filler but before the node representation.
            end: Suffix string inserted after the children representations.

        Raises:
            TypeError: If a child node is not an instance of `ASTNode`.

        Returns:
            The pretty string representation.
        """

        first_row = fill * level + pre + (f"{self!r}")
        if self.is_leaf():
            # don't open parenthesis
            return first_row + end

        childs = ""
        for child in self.children:
            if isinstance(child, ASTNode):
                pre_child = ""
                end_child = ""
                # field names are like "name" and "body" in the FunctionDefinition node.
                if hasattr(child, "field_name"):
                    pre_child = child.field_name + "="
                    end_child = ",\n" if id(child) != id(self.children[-1]) else ""
                child_repr = child.get_node_repr(level + 1, fill, pre_child, end_child)
                childs += child_repr
            else:
                raise TypeError(f"Expected ASTNode, but got {type(child).__name__}")

        last_row = fill * level + ")" + end
        return f"{first_row}(\n{childs}\n{last_row}"


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
        self.field_name: str | None = None


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
        self.field_name: str | None = None

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


def generate_pretty_ast_repr(tree: Tree) -> str:
    """Generates a pretty string representation for a parse tree.

    Args:
        tree: The parse tree.

    Returns:
        The pretty string representation.
    """

    fill = "   "
    root: ASTNode = tree.root
    return root.get_node_repr(0, fill)
