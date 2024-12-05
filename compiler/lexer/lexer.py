import re
from enum import Enum
from typing import Any

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

    def __init__(self, token_type: TokenType, value: Any = None) -> None:
        self._type = token_type
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    def __repr__(self) -> str:
        return self._type.name


def tokenize(c_source_file: str) -> list[Token]:
    """Tokenizes the contents of a C source file as part of the lexer component.

    This function is responsible for the lexical analysis phase of the compiler.
    It reads the specified C source file, breaks its content into a sequence of
    tokens, and classifies them as keywords, identifiers, operators, literals, etc.

    Args:
        c_source_file: Path to the C source file.

    Raises:
        ValueError: If an unrecognized sequence is encountered in the source code.

    Returns:
        A list of tokens representing the syntactic elements of the source file.
    """
    logger.info(f"Running lexer on file '{c_source_file}'...")

    output_tokens: list[Token] = []

    with open(c_source_file) as file:
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
                tok = Token(token_type, token_value)
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
