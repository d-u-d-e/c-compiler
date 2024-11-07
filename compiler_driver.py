#!/usr/bin/env python3

import os
import subprocess
import argparse
from tempfile import NamedTemporaryFile
from loguru import logger
import lexer


def gcc_preprocess(input_file: str, output_file: NamedTemporaryFile) -> None:
    """Preprocess a C source file using GCC and save the result to a specified output file.

    Args:
        input_file: Path to the source C file to preprocess.
        output_file: A temporary file object where the preprocessed
            output will be saved. The file has a `.i` extension.
    """
    logger.info(f"Preprocessing C source file '{input_file}'...")
    subprocess.run(["gcc", "-E", "-P", input_file, "-o", output_file.name], check=True)


def compile(
    input_file: NamedTemporaryFile, output_file: NamedTemporaryFile, use_gcc: bool
) -> None:
    """Compiles a preprocessed C source file into an assembly file.

    Args:
        input_file: A temporary file object representing the preprocessed C file.
            The file must have a `.i` extension.
        output_file: A temporary file object where the compiled assembly output will be saved.
            The file has a `.s` extension.
    """
    logger.info(f"Compiling preprocessed file '{input_file.name}'...")
    if use_gcc:
        subprocess.run(
            [
                "gcc",
                "-S",
                "-O",
                "-fno-asynchronous-unwind-tables",
                "-fcf-protection=none",
                input_file.name,
                "-o",
                output_file.name,
            ],
            check=True,
        )
    else:
        # TODO: Implement your compiler
        pass


def gcc_assemble_and_link(input_file: NamedTemporaryFile, output_file: str) -> None:
    """Assembles and links an assembly file to produce an executable.

    Args:
        input_file: A temporary file object representing the assembly file to be assembled and linked.
            The file must have a `.s` extension.
        output_file: Path where the resulting executable will be saved.
    """
    logger.info(f"Assembling and linking assembly file '{input_file.name}'...")
    subprocess.run(["gcc", input_file.name, "-o", output_file], check=True)


def cfile_type(s: str) -> str:
    """Checks if a given string is a valid C source file path.

    Args:
        s: The path to the file as a string.

    Returns:
        str: The original string if it represents a valid C source file.
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

    if args.lex:
        # TODO: Run the lexer, but stop before parsing
        lexer.run(INPUT_FILE)
        exit(0)
    elif args.parse:
        # TODO: Run the lexer and parser, but stop before assembly generation
        exit(0)
    elif args.codegen:
        # TODO: Perform lexing, parsing, and assembly generation, but stop before code emission
        exit(0)

    # Create temporary files
    preprocessed_file = NamedTemporaryFile(suffix=".i")
    assembly_file = NamedTemporaryFile(suffix=".s")

    # Execute compiler driver's commands
    try:
        gcc_preprocess(INPUT_FILE, preprocessed_file)

        compile(preprocessed_file, assembly_file, use_gcc=True)

        gcc_assemble_and_link(assembly_file, OUTPUT_FILE)
    except subprocess.CalledProcessError as e:
        return e.returncode

    preprocessed_file.close()
    assembly_file.close()

    exit(0)


if __name__ == "__main__":
    main()
