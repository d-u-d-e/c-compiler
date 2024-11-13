from abc import abstractmethod
from lib.tree.node import TreeNode


class Exp(TreeNode):
    @abstractmethod
    def __init__(self, parent: TreeNode, **kwargs):
        super().__init__(parent, **kwargs)


class Statement(TreeNode):
    @abstractmethod
    def __init__(self, parent: TreeNode, **kwargs):
        super().__init__(parent, **kwargs)

class Program(TreeNode):
    def __init__(self):
        super().__init__()

class Identifier(TreeNode):
    def __init__(self, parent: TreeNode, name: str):
        super().__init__(parent)
        self.name = name


class FunctionDefinition(TreeNode):
    def __init__(self, parent: TreeNode, name: Identifier, body: Statement):
        super().__init__(parent)
        self.name = name
        self.body = body


class Return(Statement):
    def __init__(self, parent: TreeNode):
        super().__init__(parent)


class Constant(Exp):
    def __init__(self, parent: TreeNode, value):
        super().__init__(parent)
        self.value = value
