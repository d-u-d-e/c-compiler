from .node import TraversalMode, TreeNode


class Tree:
    def __init__(self, root: TreeNode | None) -> None:
        self._root = root

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: TreeNode):
        self._root = value

    def __len__(self):
        if self._root is None:
            return 0
        return len(list(self.traverse()))

    def traverse(self, mode: TraversalMode = TraversalMode.DEPTH_FIRST):
        if self._root is None:
            raise RuntimeError("Tree is empty")
        return self._root.traverse(mode)
