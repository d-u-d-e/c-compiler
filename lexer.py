import re
from loguru import logger


def run(c_source_file: str) -> None:
    """Read in a C source file and produce a list of tokens.

    Args:
        c_source_file: path to the C source file
    """
    logger.info(f"Running lexer on file '{c_source_file}...'")
    token_regex = {
        "Identifier": r"[a-zA-Z_]\w*\b",
        "Constant": r"[0-9]+\b",
        "int keyword": r"int\b",
        "void keyword": r"void\b",
        "return keyword": r"return\b",
        "Open parenthesis": r"\(",
        "Close parenthesis": r"\)",
        "Open brace": r"{",
        "Close brace": r"}",
        "Semicolon": r";",
    }

    token_list = []

    with open(c_source_file, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break

            while len(line) > 0:
                # Trim whitespaces from start of line
                line = line.lstrip()

                check = False
                # Find longest match at start of line for any regex
                for regex in token_regex:
                    match = re.match(token_regex[regex], line)
                    if match:
                        token_list.append(match.group())
                        # Remove match from line
                        line = line[match.end() :]
                        check = True
                        break

                if not check:
                    raise ValueError(
                        f"The start of the string '{line}' doesn’t match the regular expression for any token"
                    )
        print(token_list)
