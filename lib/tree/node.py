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
        TreeNode = self
        while TreeNode is not None:
            yield TreeNode
            TreeNode = TreeNode.parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value: "TreeNode"):
        if value and not isinstance(value, TreeNode):
            raise ValueError("Parent must be instance of TreeNode")
        # make sure we don't set the parent to a descendant of self
        self.__check_loop(value)
        # update pointers
        self.__detach(self.parent)
        self.__attach(value)

    def __detach(self, parent: "TreeNode"):
        if parent is not None:
            parent.children.remove(self)
        self._parent = None

    def __attach(self, parent: "TreeNode"):
        if parent is not None:
            parent.children.append(self)
        self._parent = parent

    def __check_loop(self, TreeNode: "TreeNode"):
        if TreeNode is None:
            return
        elif any(v is self for v in TreeNode.iter_path_root()):
            raise RuntimeError("%r is ancestor of %r" % (self, TreeNode))

    def is_leaf(self) -> bool:
        return len(self._children) == 0


