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
        self.field_name: str | None = None

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
            # Don't open parenthesis
            return first_row + end

        children_repr = ""
        for child in self.children:
            if isinstance(child, ASTNode):
                pre_child = ""
                end_child = ",\n" if id(child) != id(self.children[-1]) else ""
                # Field names are like "name" and "body" in the Function node.
                if child.field_name is not None:
                    pre_child = child.field_name + "="
                child_repr = child.get_node_repr(level + 1, fill, pre_child, end_child)
                children_repr += child_repr
            else:
                raise TypeError(f"Expected ASTNode, but got {type(child).__name__}")

        last_row = fill * level + ")" + end
        return f"{first_row}(\n{children_repr}\n{last_row}"


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
