import compiler.assembly_generation.assembly_ast as assembly_ast
from lib.tree.tree import Tree


def emit_assembly_code(input_tree: Tree, output_path: str) -> str:
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
    header_line = "\t.intel_syntax noprefix\n"
    function_code = translate_function(program.function_definition)
    # The following line indicates that the code won't need an executable stack
    ending_line = '\t.section .note.GNU-stack,"",@progbits\n'
    return header_line + function_code + ending_line


def translate_function(function: assembly_ast.Function) -> str:
    """
    Translates a Function node to the corresponding assembly code.

    :param function: The Function node to translate
    :return: A string with the corresponding assembly code
    """
    func_identifier = translate_identifier(function.name)
    instructions = translate_body(function.body)
    header = f"\t.global {func_identifier}\n"
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


def translate_mov(mov_instruction: assembly_ast.Mov) -> str:
    """
    Translates a Mov node to the corresponding line of assembly code.

    :param mov_instruction: The Mov node to translate
    :raises: RuntimeError: If the operand inside the instruction is not recognized
    :raises: SyntaxError: If the destination operand is an Immediate node
    :return: A string with the corresponding line of assembly code
    """
    src, dst = "", ""
    if isinstance(mov_instruction.source, assembly_ast.Register):
        src = mov_instruction.source.name
    elif isinstance(mov_instruction.source, assembly_ast.Immediate):
        src = mov_instruction.source.value
    else:
        raise RuntimeError(
            f"Failed to translate operand '{mov_instruction.source}' inside move instruction"
        )

    if isinstance(mov_instruction.destination, assembly_ast.Register):
        dst = mov_instruction.destination.name
    elif isinstance(mov_instruction.destination, assembly_ast.Immediate):
        raise SyntaxError(
            f"Cannot use Immediate operand '{mov_instruction.destination}' as destination for a move instruction"
        )
    else:
        raise RuntimeError(
            f"Failed to translate operand '{mov_instruction.destination}' inside move instruction"
        )
    return f"mov\t{dst}, {src}\n"
