import compiler.assembly_generation.ast as assembly_ast
from lib.tree.tree import Tree


def add_comment(comment: str, on_new_line=False) -> str:
    if comment == "":
        return ""
    # If the provided input is a text written on multiple lines, '#' symbol is added in front of each line
    new_comment = comment.replace("\n", "\n#")
    if on_new_line:
        return f"\n#{new_comment}\n"
    else:
        return f"\t#{new_comment}"


def write_assembly_code(input_tree: Tree, output_path: str) -> str:
    """
    Translates the input assembly AST to the corresponding assembly code,
    then writes it into the file whose path is received as the second input.

    :param input_tree: The assembly AST to be translated
    :param output_path: The string containing the file path in which to write the assembly code
    :raises: TypeError: If the root node of the parse tree is not a Program node
    :return: A string containing the whole assembly code
    """

    if not isinstance(input_tree.root, assembly_ast.Program):
        raise TypeError(
            f"The root node of the assembly AST '{input_tree}' is not a Program node"
        )
    output_code = translate_program(input_tree.root)
    with open(output_path, "w") as f:
        f.write(output_code)
    return output_code


def translate_program(program: assembly_ast.Program) -> str:
    """
    Translates a Program node to the corresponding assembly code.

    :param program: The Program node to translate
    :return: A string with the corresponding assembly code
    """
    function_code = translate_function(program.function_definition)
    # The following line indicates that the code won't need an executable stack
    ending_line = '\t.section .note.GNU-stack,"",@progbits\n'
    return function_code + ending_line


def translate_function(function: assembly_ast.Function, comment="") -> str:
    """
    Translates a Function node to the corresponding assembly code.

    :param function: The Function node to translate
    :param comment: An optional comment to append after the .globl directive
    :return: A string with the corresponding assembly code
    """
    func_identifier = translate_identifier(function.name)
    instructions = translate_body(function.body)
    header = f"\t.globl {func_identifier}{add_comment(comment)}\n"
    label = f"{func_identifier}:\n"
    return header + label + instructions


def translate_identifier(func_name: assembly_ast.Identifier) -> str:
    """
    Translates an Identifier node to the corresponding label for the assembly code.

    :param func_name: The Identifier node to translate
    :return: A string with the identifying label
    """
    return func_name.value


def translate_body(func_body: list[assembly_ast.Instruction]) -> str:
    """
    Translates a list of Instruction nodes to the corresponding lines of assembly code.

    :param func_body: The list of Instruction nodes to translate
    :raises: RuntimeError: If one of the instructions is not recognized
    :return: A string with the corresponding assembly code
    """
    instructions_code = ""
    for instruction in func_body:
        if isinstance(instruction, assembly_ast.Mov):
            instructions_code += f"\t{translate_mov(instruction)}\n"
        elif isinstance(instruction, assembly_ast.Return):
            instructions_code += "\tret\n"
        else:
            raise RuntimeError(
                f"Failed to translate node '{instruction}' into a valid assembly instruction"
            )
    return instructions_code


def translate_mov(mov_instruction: assembly_ast.Mov, comment="") -> str:
    """
    Translates a Mov node to the corresponding line of assembly code.

    :param mov_instruction: The Mov node to translate
    :param comment: An optional comment to append to the line of code
    :raises: RuntimeError: If the operand inside the instruction is not recognized
    :return: A string with the corresponding line of assembly code
    """
    mov_code = "movl\t"
    for child in mov_instruction.children:
        if isinstance(child, assembly_ast.Immediate):
            mov_code += f"${child.value}, "
        elif isinstance(child, assembly_ast.Register):
            mov_code += f"%{child.name}, "
        else:
            raise RuntimeError(
                f"Failed to translate operand '{child}' inside move instruction"
            )
    # The spare ", " is excluded from the final instruction line
    return f"{mov_code[:-2]}{add_comment(comment)}"
