import os

import compiler.assembly_generation.ast as assembly_ast
import compiler.parser.ast as parser_ast
from lib.tree.tree import Tree


def generate_assembly_ast(parse_tree: Tree) -> Tree:
    """
    Converts a parse tree rooted at a Program node into an Assembly AST tree.

    :param parse_tree: The parse tree to convert
    :raises: TypeError: If the root node of the parse tree is not a Program node
    :return: An Assembly AST tree
    """
    if not isinstance(parse_tree.root, parser_ast.Program):
        raise TypeError(
            f"The root node of the parse tree '{parse_tree}' is not a Program node"
        )
    prog = convert_program(parse_tree.root)
    return Tree(prog)


def convert_program(prog: parser_ast.Program) -> assembly_ast.Program:
    """
    Converts a parser Program node into an assembly Program node.

    This function takes a Program node, converts its function definition
    into an assembly Function node, and then wraps it into an assembly
    Program node.

    :param prog: The parser Program node to convert
    :return: An assembly Program node
    """
    ast_func_def = convert_function_definition(prog.function_definition)
    ast_prog = assembly_ast.Program(ast_func_def)
    return ast_prog


def convert_function_definition(func_def: parser_ast.Function) -> assembly_ast.Function:
    """
    Converts a parser Function node into an assembly Function node.

    This function takes a Function node, converts its body Statement into a list
    of Assembly instructions, and its name Identifier into an assembly Identifier
    node.

    :param func_def: The parser Function node to convert
    :return: An assembly Function node
    """
    instructions = convert_statement(func_def.body)
    name = convert_identifier(func_def.name)
    return assembly_ast.Function(parent=None, body=instructions, identifier=name)


def convert_statement(
    statement: parser_ast.Statement,
) -> list[assembly_ast.Instruction]:
    """
    Converts a parser Statement node into a list of Assembly instructions.

    :param statement: The Statement node to convert
    :raises: RuntimeError: If the statement type is not supported
    :return: A list of Assembly instructions
    """

    if isinstance(statement, parser_ast.Return):
        return convert_return_statement(statement)
    else:
        raise RuntimeError(
            f"Node '{statement}' cannot be converted into a list of Assembly instructions"
        )


def convert_return_statement(
    return_statement: parser_ast.Return,
) -> list[assembly_ast.Instruction]:
    """
    Converts a Return statement into a list of Assembly instructions.

    The instruction list consists of a single Mov instruction and a Return instruction.
    The Mov instruction moves the value of the return expression into the register eax.

    :param return_statement: The Return statement to convert
    :return: A list of Assembly instructions
    """
    # This assumes that the return expression is an assembly operand
    return [
        assembly_ast.Mov(
            parent=None,
            source=convert_expression(return_statement.exp),
            # Currently the only used register is eax
            destination=assembly_ast.Register(parent=None, name="eax"),
        ),
        assembly_ast.Return(parent=None),
    ]


def convert_expression(exp: parser_ast.Exp) -> assembly_ast.Operand:
    """
    Converts an expression into an Assembly operand.

    If the expression is a Constant, it returns an Immediate node with the same value.

    :param exp: The expression to convert
    :raises: RuntimeError: If the expression type is not supported
    :return: An Assembly operand
    """
    if isinstance(exp, parser_ast.Constant):
        return assembly_ast.Immediate(parent=None, value=exp.value)
    else:
        raise RuntimeError(f"Node '{exp}' cannot be converted to Assembly Operand node")


def convert_identifier(func_name: parser_ast.Identifier) -> assembly_ast.Identifier:
    """
    Converts a parser Identifier node into an assembly Identifier node.

    :param func_name: The parser Identifier node to convert
    :return: An assembly Identifier node with the same value
    """
    return assembly_ast.Identifier(parent=None, value=func_name.value)


def emit_assembly_code(input_tree: Tree, input_file: str):
    """Writes the output assembly code into a .s file stored in the folder compiler/assembly_generation/output/.

    Args:
        tree: Assembly AST to be translated in assembly code.
        input_file: String containing the file path of the source code in c.

    Raises:
        AttributeError: If a node does not feature the required assembly representation.
    """
    filename = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "output", f"{filename}.s"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Calling the depth-first traversal of the assembly AST
    nodes = input_tree.traverse()
    nodes_iter = iter(nodes)
    to_print = ""
    with open(output_path, "w") as f:
        for node in nodes_iter:
            if isinstance(node, assembly_ast.Function):
                to_print += f"\tglobl.\t{node.name.value}\n"
                to_print += f"{node.name.value}:\n"
                for instruction in node.body:
                    # Defining the syntax for an instruction in assembly
                    if callable(getattr(instruction, "assembly_repr", None)):
                        instr_line = f"{instruction.assembly_repr()}\t"  # type: ignore
                    else:
                        raise AttributeError(
                            f'Method "assembly_repr()" not found for object of type {type(instruction).__name__}.'
                        )
                    if instruction.is_leaf():
                        # Removing the ending tab
                        instr_line = instr_line[:-1]
                    else:
                        for operand in instruction.children:
                            if callable(getattr(operand, "assembly_repr", None)):
                                instr_line += f"${operand.assembly_repr()}, "  # type: ignore
                            else:
                                raise AttributeError(
                                    f'Method "assembly_repr()" not found for object of type {type(operand).__name__}.'
                                )
                            next(nodes_iter, None)
                        # Removing the ending ", " characters
                        instr_line = instr_line[:-2]
                    to_print += f"\t{instr_line}\n"
                    next(nodes_iter, None)
                next(nodes_iter, None)
        to_print += '\t.section .note.GNU-stack,"",@progbits'
        f.write(to_print)
