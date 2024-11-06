import os
import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        raise ValueError("Provide the path to the C source file.")
    elif len(sys.argv) > 3:
        raise ValueError(
            "Too many arguments: please provide only the path to the C source file and/or 1 option between '--lex', '--parse', '--codegen'"
        )

    INPUT_FILE = sys.argv[1]

    # Ensure input file has a .c extension
    if not INPUT_FILE.endswith(".c"):
        raise ValueError("The input file must have a .c extension.")

    # Check for options
    if len(sys.argv) == 3:
        if "--lex" in sys.argv:
            # TODO: run the lexer, but stop before parsing
            sys.exit(0)
        elif "--parse" in sys.argv:
            # TODO: run the lexer and parser, but stop before assembly generation
            sys.exit(0)
        elif "--codegen" in sys.argv:
            # TODO: perform lexing, parsing, and assembly generation, but stop before code emission
            sys.exit(0)
        else:
            raise ValueError(
                f"Unknown option: {sys.argv[2]}. Options available: [--lex, --parse, --codegen]"
            )

    # Create file names
    OUTPUT_FILE, _ = os.path.splitext(INPUT_FILE)
    ASSEMBLY_FILE = f"{OUTPUT_FILE}.s"
    PREPROCESSED_FILE = f"{OUTPUT_FILE}.i"

    # Execute compiler driver's commands
    try:
        # This command preprocesses INPUT_FILE and then writes the result to PREPROCESSED_FILE
        subprocess.run(
            ["gcc", "-E", "-P", INPUT_FILE, "-o", PREPROCESSED_FILE], check=True
        )

        # Compile the preprocessed source file and output an assembly file
        # TODO: create your own compiler!
        subprocess.run(
            [
                "gcc",
                "-S",
                "-O",
                "-fno-asynchronous-unwind-tables",
                "-fcf-protection=none",
                PREPROCESSED_FILE,
            ],
            check=True,
        )

        # Assemble and link the assembly file to produce an executable
        subprocess.run(["gcc", ASSEMBLY_FILE, "-o", OUTPUT_FILE], check=True)
    except subprocess.CalledProcessError as e:
        return e.returncode

    # Remove intermidiate files
    os.remove(PREPROCESSED_FILE)
    os.remove(ASSEMBLY_FILE)

    sys.exit(0)


if __name__ == "__main__":
    main()
