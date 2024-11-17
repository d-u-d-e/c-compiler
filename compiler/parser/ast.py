from abc import abstractmethod
from lib.tree.node import TreeNode
from lib.tree.tree import Tree


class ASTNode(TreeNode):
    """Abstract class denoting a generic AST node.

    All nodes shares the `get_node_repr` method to obtain a pretty
    representation rooted at `self`.
    """

    @abstractmethod
    def __init__(self, parent: "ASTNode" = None, **kwargs):
        super().__init__(parent, **kwargs)

    # TODO: can we make this more clean?
    def get_node_repr(self, level: int, fill: str, pre: str = "", end: str = "") -> str:
        """Gets the subtree representation rooted at `self`.

        Args:
            level: integer representing the level of the subtree at this node.
            fill: indicates which string to use as a filler to make the representation look pretty.
            pre: prefix string inserted after the filler but before the node representation.
            end: suffix string inserted after the children representations.

        Returns:
            The pretty string representation.
        """

        first_row = fill * level + pre + (f"{self!r}")
        if self.is_leaf():
            # don't open parenthesis
            return first_row + end

        childs = ""
        child: ASTNode
        for child in self.children:
            pre_child = ""
            end_child = ""
            # field names are like "name" and "body" in the FunctionDefinition node.
            if hasattr(child, "field_name"):
                pre_child = getattr(child, "field_name") + "="
                end_child = ",\n" if id(child) != id(self.children[-1]) else ""
            child_repr = child.get_node_repr(level + 1, fill, pre_child, end_child)
            childs += child_repr

        last_row = fill * level + ")" + end
        return f"{first_row}(\n{childs}\n{last_row}"


class Exp(ASTNode):
    """Abstract class denoting a generic expression."""

    @abstractmethod
    def __init__(self, parent: ASTNode, **kwargs):
        super().__init__(parent, **kwargs)


class Statement(ASTNode):
    """Abstract class denoting a generic statement."""

    @abstractmethod
    def __init__(self, parent: ASTNode, **kwargs):
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

    def __init__(self, parent: ASTNode, name: str):
        super().__init__(parent)
        self.name = name

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


class FunctionDefinition(ASTNode):
    """A function definition has a name identifier and a body.
    Currently arguments are not supported.
    """

    def __init__(self, parent: ASTNode, name: Identifier, body: Statement):
        super().__init__(parent)
        name.parent = self
        body.parent = self
        # used by get_node_repr to prefix the representation of each child with
        # "name=...", "body=..."
        setattr(name, "field_name", "name")
        setattr(body, "field_name", "body")

    def __repr__(self) -> str:
        return "FunctionDefinition"


class Return(Statement):
    """A return statement is a statement."""

    def __init__(self, parent: ASTNode):
        super().__init__(parent)

    def __repr__(self) -> str:
        return "Return"


class Constant(Exp):
    """A constant node is an expression."""

    def __init__(self, parent: ASTNode, value):
        super().__init__(parent)
        self.value = value

    def __repr__(self) -> str:
        return f"Constant({self.value})"


def generate_pretty_ast_repr(tree: Tree) -> str:
    """Gets a pretty string representation for a parse tree.

    Args:
        tree: the parse tree.

    Returns:
        The pretty string representation.
    """

    fill = "   "
    root: ASTNode = tree.root
    return root.get_node_repr(0, fill)
