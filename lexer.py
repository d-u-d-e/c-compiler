import re
from loguru import logger


def run(c_source_file: str) -> None:
    """Read in a C source file and produce a list of tokens.

    Args:
        c_source_file: path to the C source file
    """
    logger.info(f"Running lexer on file '{c_source_file}...'")

    token_patterns = {
        "Identifier": re.compile(r"[a-zA-Z_]\w*\b"),
        "Constant": re.compile(r"[0-9]+\b"),
        "Open parenthesis": re.compile(r"\("),
        "Close parenthesis": re.compile(r"\)"),
        "Open brace": re.compile(r"{"),
        "Close brace": re.compile(r"}"),
        "Semicolon": re.compile(r";"),
    }

    token_keywords = {
        "int keyword": re.compile(r"\bint\b"),
        "void keyword": re.compile(r"\bvoid\b"),
        "return keyword": re.compile(r"\breturn\b"),
    }

    output_tokens = []

    with open(c_source_file, "r") as file:
        code = file.read()

    position = 0
    while position < len(code):
        # Trim whitespace
        code = code[position:].lstrip()
        position = 0

        matched = False

        # Check each regex pattern
        for token_type, pattern in token_patterns.items():
            match = pattern.match(code)
            if match:
                # Check if the identifier is a keyword
                if token_type == "Identifier":
                    for keyword, pattern in token_keywords.items():
                        if re.fullmatch(pattern, match.group()):
                            token_type = keyword
                token_value = match.group()
                output_tokens.append((token_type, token_value))
                # Move past the matched token
                position = match.end()
                matched = True
                break

        if not matched and len(code) > 0:
            # If no match found, report the unmatched part
            error_segment = code[:20]  # First 20 chars of the unmatched segment
            raise ValueError(f"Unrecognized sequence: '{error_segment}'")
