import re
from enum import Enum
from loguru import logger


class Token:
    """
    A class for encapsulating a lexer token and its associated pattern.

    This class encapsulates a token's type and its associated regular expression
    pattern. The token type is defined by the nested `TokenType` enumeration, which
    includes various token categories like identifiers, constants, and specific
    keywords (e.g., 'int', 'void', 'return').
    """

    class TokenType(Enum):
        Identifier = 0
        Constant = 1
        OpenParenthesis = 2
        CloseParenthesis = 3
        OpenBrace = 4
        CloseBrace = 5
        Semicolon = 6
        IntKeyword = 7
        VoidKeyword = 8
        ReturnKeyword = 9

        def __repr__(self) -> str:
            return self.name

    token_patterns = {
        TokenType.Identifier: re.compile(r"[a-zA-Z_]\w*\b"),
        TokenType.Constant: re.compile(r"[0-9]+\b"),
        TokenType.OpenParenthesis: re.compile(r"\("),
        TokenType.CloseParenthesis: re.compile(r"\)"),
        TokenType.OpenBrace: re.compile(r"{"),
        TokenType.CloseBrace: re.compile(r"}"),
        TokenType.Semicolon: re.compile(r";"),
    }

    token_keywords = {
        TokenType.IntKeyword: re.compile(r"\bint\b"),
        TokenType.VoidKeyword: re.compile(r"\bvoid\b"),
        TokenType.ReturnKeyword: re.compile(r"\breturn\b"),
    }

    def __init__(self, token_type: TokenType) -> None:
        self._type = token_type
        self._value = None

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self) -> str:
        return self._type.name


def run(c_source_file: str) -> list[Token]:
    """Reads in a C source file and produces a list of tokens.

    Args:
        c_source_file: path to the C source file

    Raises:
        ValueError: If no match is found for a sequence in the source code

    Returns:
        A list of tokens where each token is represented as a tuple in the format (token_type, token_value).

        - token_type: The category of the token (e.g., 'Identifier', 'Constant').
        - token_value: The actual value of the token in the C source file.
    """
    logger.info(f"Running lexer on file '{c_source_file}'...")

    output_tokens = []

    with open(c_source_file, "r") as file:
        code = file.read()

    position = 0
    while position < len(code):
        # Trim whitespace
        code = code[position:].lstrip()
        if len(code) == 0:
            break
        position = 0
        matched = False

        # Check each regex pattern
        for token_type, pattern in Token.token_patterns.items():
            match = pattern.match(code)
            if match:
                # Check if the identifier is a keyword
                if token_type == Token.TokenType.Identifier:
                    for keyword, pattern in Token.token_keywords.items():
                        if re.fullmatch(pattern, match.group()):
                            token_type = keyword
                token_value = match.group()
                tok = Token(token_type)
                tok.value = token_value
                output_tokens.append(tok)
                # Move past the matched token
                position = match.end()
                matched = True
                break

        if not matched:
            # If no match found, report the unmatched part
            error_segment = code[:20]  # First 20 chars of the unmatched segment
            raise ValueError(f"Unrecognized sequence: '{error_segment}'")

    return output_tokens
