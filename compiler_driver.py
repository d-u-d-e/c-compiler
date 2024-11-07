import os
import subprocess
import sys
import argparse


def gcc_preprocess(input_file: str, output_file: str) -> None:
    """Preprocesses a C source file using gcc, and then writes the result to an output file.

    Args:
        input_file: Path to the source C file to preprocess.
        output_file: Path where the preprocessed output will be saved. By convention, it should have a `.i` file extension.
    """
    subprocess.run(["gcc", "-E", input_file, "-o", output_file], check=True)


def compile(input_file: str, output_file: str) -> None:
    """Compiles a preprocessed C source file into an assembly file.

    Args:
        input_file: Path to the preprocessed C file. This file should have a `.i` extension.
        output_file: Path to the assembly output file.
    """
    # TODO: Implement the compiler
    pass


def gcc_assemble_and_link(input_file: str, output_file: str) -> None:
    """Assembles and links an assembly file to produce an executable.

    Args:
        input_file: Path to the assembly file to be assembled and linked.
        output_file: Path where the resulting executable will be saved.
    """
    subprocess.run(["gcc", input_file, "-o", output_file], check=True)


def main():
    # Set up argparse for argument parsing
    parser = argparse.ArgumentParser()

    # Required input file argument
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the C source file (must have a .c extension).",
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

    if args.lex:
        # TODO: Run the lexer, but stop before parsing
        sys.exit(0)
    elif args.parse:
        # TODO: Run the lexer and parser, but stop before assembly generation
        sys.exit(0)
    elif args.codegen:
        # TODO: Perform lexing, parsing, and assembly generation, but stop before code emission
        sys.exit(0)

    INPUT_FILE = args.input_file

    # Create file names
    OUTPUT_FILE, _ = os.path.splitext(INPUT_FILE)
    ASSEMBLY_FILE = f"{OUTPUT_FILE}.s"
    PREPROCESSED_FILE = f"{OUTPUT_FILE}.i"

    # Execute compiler driver's commands
    try:
        gcc_preprocess(INPUT_FILE, PREPROCESSED_FILE)

        compile(PREPROCESSED_FILE, ASSEMBLY_FILE)

        gcc_assemble_and_link(ASSEMBLY_FILE, OUTPUT_FILE)
    except subprocess.CalledProcessError as e:
        return e.returncode

    # Remove intermidiate files
    os.remove(PREPROCESSED_FILE)
    os.remove(ASSEMBLY_FILE)

    sys.exit(0)


if __name__ == "__main__":
    main()
