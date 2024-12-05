#!/usr/bin/env -S python3

import argparse
import os
import subprocess
from tempfile import NamedTemporaryFile

from loguru import logger

from compiler.assembly_generation.assembly_generation import generate_assembly_ast
from compiler.lexer import lexer
from compiler.parser import parser
from lib.ast.ast import generate_pretty_ast_repr


def gcc_preprocess(input_file: str, output_file: str) -> None:
    """Preprocess a C source file using GCC and saves the result to a specified output file.

    Args:
        input_file: Path to the source C file to preprocess.
        output_file: Path to the preprocessed file. The file should have `.i` extension.
    """
    logger.info(f"Preprocessing C source file '{input_file}'...")
    subprocess.run(["gcc", "-E", "-P", input_file, "-o", output_file], check=True)


def run_compiler(input_file: str, output_file: str, use_gcc: bool) -> None:
    """Compiles a preprocessed C source file into an assembly file.

    Args:
        input_file: Path to the preprocessed C file. The file should have a `.i` extension.
        output_file: Path to the compiled assembly file. The file should have a `.s` extension.
    """
    logger.info(f"Compiling preprocessed file '{input_file}'...")
    if use_gcc:
        subprocess.run(
            [
                "gcc",
                "-S",
                "-O",
                "-fno-asynchronous-unwind-tables",
                "-fcf-protection=none",
                input_file,
                "-o",
                output_file,
            ],
            check=True,
        )
    else:
        # TODO: Implement your compiler
        # 1. Lexer
        # 2. Parser
        # 3. Assembly generation
        # 4. Code emission
        pass


def run_compiler_stages(input_file: str, stage: str) -> None:
    """Runs specified stages of the compiler based on input arguments.

    This function preprocesses the input file and, depending on `stage`,
    performs lexing, parsing, and code generation stages. It stops at the highest
    requested stage:
    - `lex`: Performs lexing only.
    - `parse`: Performs lexing and parsing.
    - `codegen`: Performs lexing, parsing, and code generation, stopping before code emission.

    Args:
        input_file: The path to the input C source file.
        stage: Last stage to execute. Can be "lex", "parse" or "codegen".

    Raises:
        subprocess.CalledProcessError: If the preprocessing step using GCC fails.
        ValueError: If `stage` is not one of the expected values.
        NotImplementedError: If a stage has not yet be implemented. TODO: Remove after completing Chapter 1
    """
    stages = ["lex", "parse", "codegen"]
    if stage not in stages:
        raise ValueError(
            f"Invalid stage '{stage}'. Please choose 'lex', 'parse', or 'codegen'."
        )

    with NamedTemporaryFile(suffix=".i") as preprocessed_file:
        try:
            gcc_preprocess(input_file, preprocessed_file.name)
        except subprocess.CalledProcessError as e:
            exit(e.returncode)

        # Execute sequentially the stages
        tokens = []
        parse_tree = None
        for current_stage in stages:
            if current_stage == "lex":
                tokens = lexer.tokenize(preprocessed_file.name)
            elif current_stage == "parse":
                parse_tree = parser.generate_parse_tree(tokens)
                logger.debug("Parse tree:\n" + generate_pretty_ast_repr(parse_tree))
            elif current_stage == "codegen":
                assert parse_tree is not None
                assembly_ast = generate_assembly_ast(parse_tree)
                logger.debug("Assembly AST:\n" + generate_pretty_ast_repr(assembly_ast))

            # Stop once we've reached the chosen stage
            if current_stage == stage:
                break


def gcc_assemble_and_link(input_file: str, output_file: str) -> None:
    """Assembles and links an assembly file to produce an executable.

    Args:
        input_file: Path to the the assembly file to be assembled and linked. The file should have a `.s` extension.
        output_file: Path to the executable file.
    """
    logger.info(f"Assembling and linking assembly file '{input_file}'...")
    subprocess.run(["gcc", input_file, "-o", output_file], check=True)


def cfile_type(s: str) -> str:
    """Checks if a given string is a valid C source file path.

    Args:
        s: Path to the file as a string.

    Returns:
        The original string if it represents a valid C source file.
    """
    if not s.endswith(".c"):
        raise argparse.ArgumentTypeError(f"Not a valid C source file: {s!r}")
    return s


def main():
    # Set up argparse for argument parsing
    parser = argparse.ArgumentParser()

    # Required input file argument
    parser.add_argument(
        "input_file",
        type=cfile_type,
        help="Path to the C source file",
    )

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group()

    # Add the arguments to the group
    group.add_argument(
        "--lex",
        action="store_true",
        help="Run the lexer, but stop before parsing",
    )

    group.add_argument(
        "--parse",
        action="store_true",
        help="Run the lexer and parser, but stop before assembly generation",
    )

    group.add_argument(
        "--codegen",
        action="store_true",
        help="Perform lexing, parsing, and assembly generation, but stop before code emission",
    )

    # Parse the arguments
    args = parser.parse_args()

    INPUT_FILE = args.input_file
    OUTPUT_FILE, _ = os.path.splitext(INPUT_FILE)

    if args.lex or args.parse or args.codegen:
        if args.lex:
            stage = "lex"
        elif args.parse:
            stage = "parse"
        elif args.codegen:
            stage = "codegen"
        run_compiler_stages(INPUT_FILE, stage)
        exit(0)

    # Execute compiler driver's commands
    with (
        NamedTemporaryFile(suffix=".i") as preprocessed_file,
        NamedTemporaryFile(suffix=".s") as assembly_file,
    ):
        try:
            gcc_preprocess(INPUT_FILE, preprocessed_file.name)

            run_compiler(preprocessed_file.name, assembly_file.name, use_gcc=True)

            gcc_assemble_and_link(assembly_file.name, OUTPUT_FILE)
        except subprocess.CalledProcessError as e:
            return e.returncode

    exit(0)


if __name__ == "__main__":
    main()
