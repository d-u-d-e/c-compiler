from abc import abstractmethod
from lib.tree.node import TreeNode


class Program(TreeNode):
    def __init__(self):
        super().__init__()


class FunctionDefinition(TreeNode):
    def __init__(self, parent: Program, **kwargs):
        super().__init__(parent, kwargs)


class Statement(TreeNode):
    @abstractmethod
    def __init__(self, parent: FunctionDefinition, **kwargs):
        super().__init__(parent, kwargs)


class Return(Statement):
    def __init__(self, parent: FunctionDefinition, value: "Exp"):
        super().__init__(parent, value=value)


class Exp(TreeNode):
    @abstractmethod
    def __init__(self, parent: Return, **kwargs):
        super().__init__(parent, kwargs)


class Constant(Exp):
    def __init__(self, parent: Return, value: int):
        super().__init__(parent, value=value)


class Identifier(Exp):
    def __init__(self, parent: Return, value: str):
        super().__init__(parent, value=value)
