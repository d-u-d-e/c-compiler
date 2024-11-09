class TreeNode:
    def __init__(self, data=None, identifier=None):
        self.data = data
        self._identifier = identifier
        self._children = []
        self._parent_identifier = None

    def children(self):
        return self._children
    
    def add_child(self, child_identifier):
        self._children.append(child_identifier)
    
    def remove_child(self, child_identifier):
        self._children.remove(child_identifier)
    
    def set_parent(self, parent_identifier):
        self._parent_identifier = parent_identifier