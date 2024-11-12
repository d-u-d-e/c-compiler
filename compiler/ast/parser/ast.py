from abc import abstractmethod
from lib.tree.node import TreeNode


class Program(TreeNode):
    def __init__(self):
        super().__init__()


class FunctionDefinition(TreeNode):
    def __init__(self, parent: TreeNode, **kwargs):
        super().__init__(parent, kwargs)


class Statement(TreeNode):
    @abstractmethod
    def __init__(self, parent: TreeNode, **kwargs):
        super().__init__(parent, kwargs)


class Return(Statement):
    def __init__(self, parent: TreeNode):
        super().__init__(parent)


class Exp(TreeNode):
    @abstractmethod
    def __init__(self, parent: TreeNode, **kwargs):
        super().__init__(parent, kwargs)


class Constant(Exp):
    def __init__(self, parent: TreeNode, value: int):
        super().__init__(parent, value=value)


class Identifier(TreeNode):
    def __init__(self, parent: TreeNode, name: str):
        super().__init__(parent, name=name)
