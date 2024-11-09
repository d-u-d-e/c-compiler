from tree_node import TreeNode

class Tree:
    def __init__(self):
        self._nodes = {}
        self._root = None

    def __contains__(self, identifier):
        return identifier in self._nodes
    
    def __getitem__(self, key) -> TreeNode:
        try:
            return self._nodes[key]
        except KeyError:
            raise Exception(f"Node with id {key} is not in the tree")
        
    def __len__(self):
        return len(self._nodes)

    def add_node(self, node, parent=None):
        # sanity checks
        if not isinstance(node, TreeNode):
            raise Exception("'node' must be an instance of 'TreeNode'")
        if node.identifier in self._nodes:
            raise Exception(f"Node with id {node.identifier} already exists in the tree")
        
        # can pass either the identifier or the TreeNode as parent
        pid = parent.identifier if isinstance(parent, TreeNode) else parent
        if pid is None:
            if self._root is None:
                self._root = node.identifier
            else:
                raise Exception("Tree already has a root")
        elif not self.__contains__(pid):
            raise Exception(f"Parent node with id {pid} is not in the tree")
        
        # update refs
        self._nodes.update({node.identifier: node})
        self[pid].add_child(node._identifier)
        node.set_parent(pid)

    def create_node(self, identifier, parent=None, data=None):
        if identifier is None:
            raise Exception("Must pass a valid identifier")
        node = TreeNode(data=data, identifier=identifier)
        self.add_node(node, parent=parent)
        return node
    
    def children(self, node_identifier):
        return self[node_identifier].children
    
    def remove_node(self, node_identifier):
        # TODO
        pass