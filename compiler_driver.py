#!/usr/bin/env -S python3
# -*- coding: utf-8 -*-

import os
import subprocess
import argparse
from tempfile import NamedTemporaryFile
from loguru import logger

import lexer


def gcc_preprocess(input_file: str, output_file: str) -> None:
    """Preprocess a C source file using GCC and save the result to a specified output file.

    Args:
        input_file: Path to the source C file to preprocess.
        output_file: Path to the preprocessed file. The file should have `.i` extension.
    """
    logger.info(f"Preprocessing C source file '{input_file}'...")
    subprocess.run(["gcc", "-E", "-P", input_file, "-o", output_file], check=True)


def compile(input_file: str, output_file: str, use_gcc: bool) -> None:
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

    # Execute compiler driver's commands
    with NamedTemporaryFile(suffix=".i") as preprocessed_file, NamedTemporaryFile(
        suffix=".s"
    ) as assembly_file:
        try:
            gcc_preprocess(INPUT_FILE, preprocessed_file.name)

            # Just for testing purposes
            if args.lex:
                # TODO: Run the lexer, but stop before parsing
                lexer.run(preprocessed_file.name)
                exit(0)
            elif args.parse:
                # TODO: Run the lexer and parser, but stop before assembly generation
                exit(0)
            elif args.codegen:
                # TODO: Perform lexing, parsing, and assembly generation, but stop before code emission
                exit(0)

            compile(preprocessed_file.name, assembly_file.name, use_gcc=True)

            gcc_assemble_and_link(assembly_file.name, OUTPUT_FILE)
        except subprocess.CalledProcessError as e:
            return e.returncode

    exit(0)


if __name__ == "__main__":
    main()
