import compiler.assembly_generation.ast as assembly_ast
import compiler.parser.ast as parser_ast
from lib.tree.tree import Tree


def convert_expression(exp: parser_ast.Exp) -> assembly_ast.Operand:
    if isinstance(exp, parser_ast.Constant):
        return assembly_ast.Immediate(parent=None, value=exp.value)
    else:
        raise RuntimeError(f"Node {exp} cannot be converted to Assembly Operand node")


def convert_return_statement(stmt: parser_ast.Return) -> list[assembly_ast.Instruction]:
    # This assumes that the return expression is an assembly operand
    return [
        assembly_ast.Mov(
            parent=None,
            source=convert_expression(stmt.exp),
            # Currently the only used register is eax
            destination=assembly_ast.Register(parent=None, name="eax"),
        ),
        assembly_ast.Return(parent=None),
    ]


def convert_statement(stmt: parser_ast.Statement) -> list[assembly_ast.Instruction]:
    if isinstance(stmt, parser_ast.Return):
        return convert_return_statement(stmt)
    else:
        raise RuntimeError(
            f"Node {stmt} cannot be converted into a list of Assembly instructions"
        )


def convert_identifier(func_name: parser_ast.Identifier) -> assembly_ast.Identifier:
    return assembly_ast.Identifier(parent=None, value=func_name.value)


def convert_function_definition(func_def: parser_ast.Function):
    instructions = convert_statement(func_def.body)
    name = convert_identifier(func_def.name)
    return assembly_ast.Function(parent=None, body=instructions, identifier=name)


def convert_program(prog: parser_ast.Program):
    ast_func_def = convert_function_definition(prog.function_definition)
    ast_prog = assembly_ast.Program(ast_func_def)
    return ast_prog


def generate_assembly_ast(parse_tree: Tree) -> Tree:
    if not isinstance(parse_tree.root, parser_ast.Program):
        raise RuntimeError("Parse tree root node is not a Program node")
    prog = convert_program(parse_tree.root)
    return Tree(prog)
