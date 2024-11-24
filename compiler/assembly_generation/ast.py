from abc import abstractmethod

from lib.ast.ast import ASTNode


class Instruction(ASTNode):
    """Abstract class denoting a generic assembly instruction."""

    @abstractmethod
    def __init__(self, parent: ASTNode | None, **kwargs):
        super().__init__(parent, **kwargs)


class Operand(ASTNode):
    """Abstract class denoting a generic assembly operand."""

    @abstractmethod
    def __init__(self, parent: ASTNode | None, **kwargs):
        super().__init__(parent, **kwargs)


class Program(ASTNode):
    """The program node is the root of the parse tree."""

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return "Program"


class Identifier(ASTNode):
    """An identifier is a string, such as the name of a label."""

    def __init__(self, parent: ASTNode | None, name: str):
        super().__init__(parent)
        self.name = name

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


class FunctionDefinition(ASTNode):
    """A function definition has a name identifier and a list of instructions as its body."""

    def __init__(
        self,
        parent: ASTNode | None,
        identifier: Identifier,
        body: list[Instruction],
    ):
        super().__init__(parent)
        self._body = body
        self._name = identifier
        identifier.parent = self
        for inst in body:
            inst.parent = self
        identifier.field_name = "name"

    @property
    def name(self) -> Identifier:
        return self._name

    @property
    def body(self) -> list[Instruction]:
        return self._body

    def __repr__(self) -> str:
        return "FunctionDefinition"


class Return(Instruction):
    """A return instruction is an assembly instruction."""

    def __init__(self, parent: ASTNode | None):
        super().__init__(parent)

    def __repr__(self) -> str:
        return "Return"


class Mov(Instruction):
    """A mov instruction is an assembly instruction."""

    def __init__(self, parent: ASTNode | None, source: Operand, destination: Operand):
        super().__init__(parent)
        source.parent = self
        destination.parent = self
        source.field_name = "src"
        destination.field_name = "dst"

    def __repr__(self) -> str:
        return "Mov"


class Immediate(Operand):
    """An immediate value is an operand."""

    def __init__(self, parent: ASTNode | None, value):
        super().__init__(parent)
        self.value = value

    def __repr__(self) -> str:
        return f"Immediate({self.value})"


class Register(Operand):
    """A register is an operand. It has a name such as 'eax'."""

    def __init__(self, parent: ASTNode | None, name: str):
        super().__init__(parent)
        self.name = name

    def __repr__(self) -> str:
        return f"Register({self.name})"
