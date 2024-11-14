from abc import abstractmethod
from lib.tree.node import TreeNode
from lib.tree.tree import Tree


class ASTNode(TreeNode):
    @abstractmethod
    def __init__(self, parent: "ASTNode" = None, **kwargs):
        super().__init__(parent, **kwargs)

    # TODO: can we make this more clean?
    def get_node_repr(self, level, fill, pre="", end="") -> str:
        first_row = fill * level + pre + ("%r" % self)
        if self.is_leaf():
            # don't open parenthesis
            return first_row + end

        childs = ""
        child: ASTNode
        for child in self.children:
            pre_child = ""
            end_child = ""
            if hasattr(child, "field_name"):
                pre_child = getattr(child, "field_name") + "="
                end_child = ",\n" if id(child) != id(self.children[-1]) else ""
            child_repr = child.get_node_repr(level + 1, fill, pre_child, end_child)
            childs += child_repr

        last_row = fill * level + ")" + end
        return first_row + "(" + "\n" + childs + "\n" + last_row


class Exp(ASTNode):
    @abstractmethod
    def __init__(self, parent: ASTNode, **kwargs):
        super().__init__(parent, **kwargs)


class Statement(ASTNode):
    @abstractmethod
    def __init__(self, parent: ASTNode, **kwargs):
        super().__init__(parent, **kwargs)


class Program(ASTNode):
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return "Program"


class Identifier(ASTNode):
    def __init__(self, parent: ASTNode, name: str):
        super().__init__(parent)
        self.name = name

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


class FunctionDefinition(ASTNode):
    def __init__(self, parent: ASTNode, name: Identifier, body: Statement):
        super().__init__(parent)
        name.parent = self
        body.parent = self
        setattr(name, "field_name", "name")
        setattr(body, "field_name", "body")

    def __repr__(self) -> str:
        return "FunctionDefinition"


class Return(Statement):
    def __init__(self, parent: ASTNode):
        super().__init__(parent)

    def __repr__(self) -> str:
        return "Return"


class Constant(Exp):
    def __init__(self, parent: ASTNode, value):
        super().__init__(parent)
        self.value = value

    def __repr__(self) -> str:
        return f"Constant({self.value})"


def ast_make_prettier(tree: Tree) -> str:
    # for node in tree.traverse(TraversalMode.DEPTH_FIRST):
    #    print(node)
    fill = "   "
    root: ASTNode = tree.root
    return root.get_node_repr(0, fill)
