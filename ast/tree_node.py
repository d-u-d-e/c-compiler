from enum import Enum


class NodeType(Enum):
    PROGRAM = 1
    FUNCTION = 2
    STATEMENT = 3
    EXPRESSION = 4


class TreeNode:
    def __init__(
        self,
        typology: NodeType,
        data=None,  # TODO: what type of data can be?
    ):
        self._type = typology
        self.data = data
        self._parent: TreeNode = None
        self._children: list[TreeNode] = []

    def __str__(self) -> str:
        return f"TreeNode(type={self._type}, data={self.data})"

    def get_children(self) -> list["TreeNode"]:
        return self._children

    def add_child(self, child: "TreeNode") -> None:
        self._children.append(child)

    def remove_child(self, child: "TreeNode") -> None:
        self._children.remove(child)

    def set_parent(self, parent: "TreeNode") -> None:
        self._parent = parent

    def get_parent(self) -> "TreeNode":
        return self._parent

    def is_leaf(self) -> bool:
        return len(self._children) == 0

    def is_type(self, node_type: NodeType) -> bool:
        return self._type == node_type
