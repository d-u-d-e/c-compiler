from .node import TraversalMode, TreeNode


class Tree:
    def __init__(self, root: TreeNode) -> None:
        if root is None or not isinstance(root, TreeNode):
            raise ValueError("Invalid root")
        self._root = root

    @property
    def root(self):
        return self._root

    def __len__(self):
        return len(list(self.traverse()))

    def traverse(self, mode: TraversalMode = TraversalMode.DEPTH_FIRST):
        return self._root.traverse(mode)
