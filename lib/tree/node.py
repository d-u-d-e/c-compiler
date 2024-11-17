from enum import Enum


class TraversalMode(Enum):
    DEPTH_FIRST = 0
    BREADTH_FIRST = 1


class TreeNode:
    def __init__(self, parent: "TreeNode" = None, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self._children = []
        self._parent = None
        # use the property setter for further checks
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
        # make sure we don't set the parent to a descendant of self
        self.__check_loop(parent)
        # update pointers
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
        # generator
        yield self
        queue = [c for c in self.children]
        while queue:
            yield queue[0]
            next_nodes = [c for c in queue[0].children]
            if mode == TraversalMode.DEPTH_FIRST:
                queue = next_nodes + queue[1:]
            else:
                queue = queue[1:] + next_nodes
