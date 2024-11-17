from enum import Enum
from typing import Optional


class TraversalMode(Enum):
    DEPTH_FIRST = 0
    BREADTH_FIRST = 1


class TreeNode:
    def __init__(self, parent: Optional["TreeNode"] = None, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self._children: list[TreeNode] = []
        self._parent = None
        # Use the property setter for further checks
        if parent is not None:
            self.parent = parent

    @property
    def children(self) -> list["TreeNode"]:
        return self._children

    def iter_path_root(self):
        v = self
        while v is not None:
            yield v
            v = v.parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: "TreeNode"):
        if parent and not isinstance(parent, TreeNode):
            raise ValueError("Parent must be instance of TreeNode")
        # Make sure we don't set the parent to a descendant of self
        self.__check_loop(parent)
        # Update pointers
        self.__detach(self.parent)
        self.__attach(parent)

    def __detach(self, parent: "TreeNode"):
        if parent is not None:
            parent.children.remove(self)
        self._parent = None

    def __attach(self, parent: "TreeNode"):
        if parent is not None:
            parent.children.append(self)
        self._parent = parent

    def __check_loop(self, node: "TreeNode"):
        if node is None:
            return
        elif any(v is self for v in node.iter_path_root()):
            raise RuntimeError(f"{self!r} is ancestor of {node!r}")

    def is_leaf(self) -> bool:
        return len(self._children) == 0

    def traverse(self, mode: TraversalMode = TraversalMode.DEPTH_FIRST):
        """Traverse the tree rooted at `self` using `mode` as traversal mode.
        This is a generator.

        Args:
            mode: The traversal mode employed to visit nodes.

        Returns:
            The next node to be visited.
        """
        # Generator that yields all the nodes of the tree based on a traversal mode.
        yield self
        queue = list(self.children)
        while queue:
            yield queue[0]
            next_nodes = list(queue[0].children)
            if mode == TraversalMode.DEPTH_FIRST:
                queue = next_nodes + queue[1:]
            else:
                queue = queue[1:] + next_nodes
