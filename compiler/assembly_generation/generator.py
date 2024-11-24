import compiler.assembly_generation.ast as assembly_ast
import compiler.parser.ast as parser_ast
from lib.tree.tree import Tree


def convert_expression(exp: parser_ast.Exp) -> assembly_ast.Operand:
    if isinstance(exp, parser_ast.Constant):
        return assembly_ast.Immediate(parent=None, value=exp.value)
    else:
        raise RuntimeError(
            f"Expression node {exp} cannot be converted to Assembly Operand node"
        )


def convert_statement(stmt: parser_ast.Statement) -> list[assembly_ast.Instruction]:
    if isinstance(stmt, parser_ast.Return):
        exp = stmt.children[0]
        if len(stmt.children) != 1 or not isinstance(exp, parser_ast.Exp):
            raise RuntimeError(
                "Expected Expression node as the only child of the Return node"
            )
        # the following works only if exp can be represented as a single assembly operand
        return [
            assembly_ast.Mov(
                parent=None,
                source=convert_expression(exp),
                # currently the only used register is eax
                destination=assembly_ast.Register(parent=None, name="eax"),
            ),
            assembly_ast.Return(parent=None),
        ]
    else:
        raise RuntimeError(
            f"Statement node {stmt} cannot be converted to a list of Assembly instructions"
        )


def convert_identifier(func_name: parser_ast.Identifier) -> assembly_ast.Identifier:
    return assembly_ast.Identifier(parent=None, name=func_name.name)


def convert_function_definition(func_def: parser_ast.FunctionDefinition):
    instructions = convert_statement(func_def.body)
    name = convert_identifier(func_def.name)
    return assembly_ast.FunctionDefinition(
        parent=None, body=instructions, identifier=name
    )


def convert_program(prog: parser_ast.Program):
    ast_prog = assembly_ast.Program()
    prog_child = prog.children[0]
    if (
        not isinstance(prog_child, parser_ast.FunctionDefinition)
        or len(prog.children) != 1
    ):
        raise RuntimeError(
            "Expected a FunctionDefinition node as the only child of the Program node"
        )
    ast_func_def = convert_function_definition(prog_child)
    ast_func_def.parent = ast_prog
    return ast_prog


def generate_assembly_ast(parse_tree: Tree) -> Tree:
    if not isinstance(parse_tree.root, parser_ast.Program):
        raise RuntimeError("Parse tree root node is not a Program node")
    prog = convert_program(parse_tree.root)
    return Tree(prog)
