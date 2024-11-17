from compiler.parser.ast import (
    Constant,
    Identifier,
    Return,
    Statement,
    FunctionDefinition,
    Exp,
    Program,
)
from compiler.lexer.lexer import Token
from lib.tree.tree import Tree


def expect_token_type(expected_type: Token.TokenType, tokens: list[Token]) -> Token:
    """Pops the first element out of the tokens list and compares it to the expected type.

    Args:
        expected_type: The expected token type.
        tokens: List of tokens.

    Returns:
        The popped token.

    Raises:
        SyntaxError: If the tokens list is empty or the actual token differs from the expected token.
    """
    try:
        token = tokens.pop(0)
        if token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type!r} but found {token!r}")
        return token
    except IndexError:
        raise SyntaxError(f"Expected {expected_type!r}")


def parse_identifier(tokens: list[Token]) -> Identifier:
    """Parses a list of tokens representing an identifier and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the identifier.
    """
    # example:
    # tok.type = Token.TokenType.Identifier
    # tok.value == "main"
    # -> Identifier(name="main", parent=None)
    tok = expect_token_type(Token.TokenType.Identifier, tokens)
    return Identifier(parent=None, name=tok.value)


def parse_statement(tokens: list[Token]) -> Statement:
    """Parses a list of tokens representing a statement and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the statement.
    """
    # chapter 1: the statement is a return statement
    return parse_return_statement(tokens)


def parse_function(tokens: list[Token]) -> FunctionDefinition:
    """Parses a list of tokens representing a function and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the function.
    """
    # chapter 1
    # "int" <identifier> "(" "void" ")" "{" <statement> "}"
    expect_token_type(Token.TokenType.IntKeyword, tokens)
    identifier = parse_identifier(tokens)
    expect_token_type(Token.TokenType.OpenParenthesis, tokens)
    expect_token_type(Token.TokenType.VoidKeyword, tokens)
    expect_token_type(Token.TokenType.CloseParenthesis, tokens)
    expect_token_type(Token.TokenType.OpenBrace, tokens)
    statement = parse_statement(tokens)
    expect_token_type(Token.TokenType.CloseBrace, tokens)

    func = FunctionDefinition(parent=None, name=identifier, body=statement)
    statement.parent = func
    return func


def parse_program(tokens: list[Token]) -> Program:
    """Parses a list of tokens representing a program and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the program.
    """
    main_func = parse_function(tokens)
    # no extra junk after function
    # TODO: better!
    assert len(tokens) == 0
    prog = Program()
    main_func.parent = prog
    return prog


def run(tokens: list[Token]) -> Tree:
    """Parses the list of tokens that compose the program.
    Args:
        tokens: List of tokens.

    Returns:
        The parse tree rooted at the program node.
    """
    prog = parse_program(tokens)
    return Tree(prog)


def parse_expression(tokens: list[Token]) -> Exp:
    """Parses a list of tokens representing a an expression and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the expression.
    """
    # chapter 1: the expression is a constant
    tok = expect_token_type(Token.TokenType.Constant, tokens)
    return Constant(parent=None, value=tok.value)


def parse_return_statement(tokens: list) -> Return:
    """Parses a list of tokens representing a return statement and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the Return statement.
    """
    # chapter 1: "return" <exp> ";"
    expect_token_type(Token.TokenType.ReturnKeyword, tokens)
    expr = parse_expression(tokens)
    expect_token_type(Token.TokenType.Semicolon, tokens)

    ret = Return(parent=None)
    expr.parent = ret
    return ret
