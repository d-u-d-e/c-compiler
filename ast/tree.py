from tree_node import NodeType, TreeNode


class Tree:
    def __init__(self):
        self._nodes: set[TreeNode] = []
        self._root: TreeNode = None

    def __contains__(self, node: TreeNode) -> bool:
        return node in self._nodes

    def __getitem__(self, node: TreeNode) -> TreeNode:
        if node not in self._nodes:
            raise KeyError(f"Node '{node}' is not in the tree")
        return node

    def __len__(self) -> int:
        return len(self._nodes)

    def add_node(self, node: TreeNode, parent: TreeNode = None) -> None:
        """Adds a node to the tree, either as the root or as a child of an existing node.

        If a valid `parent` is provided, the `node` is added as a child of the `parent`, and the `node`'s parent is set accordingly.

        Args:
            node: The node to add to the tree.
            parent: The parent node under which the `node` will be added.
                If `None`, the `node` will be set as the root of the tree. Defaults to None.

        Raises:
            TypeError: If `node` is not an instance of `TreeNode`, or if `parent` is provided and is not an instance of `TreeNode`.
            ValueError: If the `node` already exists in the tree, or if the tree already has a root when trying to add a root node.
            LookupError: If the `parent` node is not found in the tree.
        """
        if not isinstance(node, TreeNode):
            raise TypeError("'node' must be an instance of 'TreeNode'")
        if parent and not isinstance(parent, TreeNode):
            raise TypeError("'parent' must be an instance of 'TreeNode'")
        if node in self._nodes:
            raise ValueError(f"Node '{node}' already exists in the tree")

        if parent is None:  # If no parent is provided, it must be the root node
            if self._root is None:
                self._root = node
            else:
                raise ValueError("Tree already has a root")
        elif not self.__contains__(parent):
            raise LookupError(f"Parent node '{parent}' is not in the tree")
        else:
            parent.add_child(node)
            node.set_parent(parent)

        self._nodes.add(node)

    def create_node(self, typology: NodeType, data=None) -> TreeNode:
        """Creates a new node with the specified typology and optional data.

        Args:
            typology: The type of the node to create. Must be a valid `NodeType`.
            data: Data to store in the node. Defaults to None.

        Raises:
            TypeError: If `typology` is not a valid `NodeType`.

        Returns:
            The newly created node.
        """
        # Single Responsibility principle
        if not isinstance(typology, NodeType):
            raise TypeError("'typology' must be a valid node type")

        return TreeNode(typology, data=data)

    def children(self, node: TreeNode) -> list[TreeNode]:
        """Returns all the children of a node."""
        return node.get_children()

    def remove_node(self, node: TreeNode) -> None:
        # TODO: remove node from the tree, and remove all its successors (?)
        pass
