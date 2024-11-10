from .tree_node import TreeNode
from enum import Enum


class Tree:
    class TraversalMode(Enum):
        DEPTH_FIRST = 0
        BREADTH_FIRST = 1

    def __init__(self):
        self._nodes: set[TreeNode] = set()
        self._root: TreeNode = None

    def __contains__(self, node: TreeNode) -> bool:
        return node in self._nodes

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
            LookupError: If the `parent` node is not found in the tree when provided.
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

    def create_node(self, parent: TreeNode = None, data=None) -> TreeNode:
        """Creates a new node with optional parent and optional data.

        Args:
            parent: The parent of the new node. Defaults to None.
            data: Data to store in the node. Defaults to None.

        Raises:
            TypeError: If `parent` is provided and is not an instance of `TreeNode`.
            ValueError: If the tree already has a root when trying to add a root node.
            LookupError: If the `parent` node is not found in the tree when provided.

        Returns:
            The newly created node.
        """

        node = TreeNode(data=data)
        self.add_node(node, parent=parent)
        return node

    def traverse(
        self, node: TreeNode = None, mode: TraversalMode = TraversalMode.DEPTH_FIRST
    ):
        """Traverse the subtree rooted at `node` using `mode` as traversal mode.

        Args:
            node: The subtree to be traversed is rooted at node.
            mode: Traversal mode for the tree. Defaults to DEPTH_FIRST.

        Raises:
            ValueError: If `node` is not part of the tree.

        Returns:
            Yields the next node to be visited during the traversal.
        """

        # generator
        if node and (node not in self):
            raise ValueError("Tree does not contain 'node'")
        # start from root if node is not specified
        start = node if node else self._root
        yield start
        queue = [c for c in start.get_children()]
        while queue:
            yield queue[0]
            next_nodes = [c for c in queue[0].get_children()]
            if mode == Tree.TraversalMode.DEPTH_FIRST:
                queue = next_nodes + queue[1:]
            else:
                queue = queue[1:] + next_nodes

    def children(self, node: TreeNode) -> list[TreeNode]:
        """Returns all the children of a node."""
        return node.get_children()

    def remove_node(self, node: TreeNode) -> None:
        """Removes a node and all of its successors.

        Args:
            node: The subtree to be removed.

        Returns:
            Number of nodes removed.
        """
        if node is None:
            raise ValueError("'node' is None")

        # update backwards pointer
        parent = node.get_parent()
        if parent:
            parent.remove_child(node)

        # remove backwards and forwards pointers from all deleted nodes
        # remove nodes from the nodes set
        count = 0
        for v in self.traverse(node):
            count += 1
            # remove node from set of nodes
            self._nodes.remove(v)
            if v is self._root:
                self._root = None
            node._parent = None
            node._children = []
        return count
