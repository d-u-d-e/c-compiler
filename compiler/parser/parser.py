from compiler.lexer.lexer import Token
from compiler.parser.parser_ast import (
    Constant,
    Exp,
    Function,
    Identifier,
    Program,
    Return,
    Statement,
)
from lib.tree.tree import Tree


def generate_parse_tree(tokens: list[Token]) -> Tree:
    """Generates a parse tree from a list of tokens as part of the parser component.

    This function performs the syntactic analysis phase of the compiler.
    It takes a list of tokens produced by the lexer and constructs a parse tree,
    which represents the hierarchical structure of the program according to the grammar rules.

    Args:
        tokens: A list of tokens representing the program.

    Returns:
        The parse tree rooted at the program node.
    """
    prog = parse_program(tokens)
    return Tree(prog)


def parse_program(tokens: list[Token]) -> Program:
    """Parses a list of tokens representing a program and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the program.
    """
    main_func = parse_function(tokens)
    # No extra junk after function
    if len(tokens) != 0:
        raise SyntaxError(
            f"Program contains junk after function '{main_func.name.value}'"
        )

    prog = Program(func_def=main_func)
    return prog


def parse_function(tokens: list[Token]) -> Function:
    """Parses a list of tokens representing a function and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the function.
    """
    # By the end of chapter 1, we parse functions with the following form:
    # "int" <identifier> "(" "void" ")" "{" <statement> "}"
    expect_token_type(Token.TokenType.IntKeyword, tokens)
    identifier = parse_identifier(tokens)
    expect_token_type(Token.TokenType.OpenParenthesis, tokens)
    expect_token_type(Token.TokenType.VoidKeyword, tokens)
    expect_token_type(Token.TokenType.CloseParenthesis, tokens)
    expect_token_type(Token.TokenType.OpenBrace, tokens)
    statement = parse_statement(tokens)
    expect_token_type(Token.TokenType.CloseBrace, tokens)

    func = Function(parent=None, name=identifier, body=statement)
    statement.parent = func
    return func


def parse_statement(tokens: list[Token]) -> Statement:
    """Parses a list of tokens representing a statement and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the statement.
    """
    # By the end of chapter 1, we parse only return statements.
    return parse_return_statement(tokens)


def parse_return_statement(tokens: list) -> Return:
    """Parses a list of tokens representing a return statement and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the Return statement.
    """
    # By the end of chapter 1 we parse the return statement as follows:
    # "return" <exp> ";"
    expect_token_type(Token.TokenType.ReturnKeyword, tokens)
    expr = parse_expression(tokens)
    expect_token_type(Token.TokenType.Semicolon, tokens)

    ret = Return(parent=None, exp=expr)
    return ret


def parse_identifier(tokens: list[Token]) -> Identifier:
    """Parses a list of tokens representing an identifier and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the identifier.
    """

    tok = expect_token_type(Token.TokenType.Identifier, tokens)
    return Identifier(parent=None, value=tok.value)


def parse_expression(tokens: list[Token]) -> Exp:
    """Parses a list of tokens representing a an expression and validates the syntax.

    Args:
        tokens: List of tokens.

    Returns:
        AST node representing the expression.
    """
    # By the end of chapter 1, the parser understands only constants as expressions.
    tok = expect_token_type(Token.TokenType.Constant, tokens)
    return Constant(parent=None, value=tok.value)


def expect_token_type(expected_type: Token.TokenType, tokens: list[Token]) -> Token:
    """Pops the first element out of the tokens list and compares it to the expected type.

    Args:
        expected_type: The expected token type.
        tokens: List of tokens.

    Raises:
        SyntaxError: If the tokens list is empty or the actual token differs from the expected token.

    Returns:
        The popped token.
    """
    try:
        token = tokens.pop(0)
        if token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type!r} but found {token!r}")
        return token
    except IndexError:
        raise SyntaxError(f"Expected {expected_type!r}") from IndexError
