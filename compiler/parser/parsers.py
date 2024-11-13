from compiler.parser.ast import (
    Constant,
    Identifier,
    Return,
    Statement,
    FunctionDefinition,
    Exp,
)
from compiler.lexer.lexer import Token


def expect_token_type(expected_type: Token.TokenType, tokens: list[Token]) -> Token:
    try:
        token = tokens.pop(0)
        if token.type != expected_type:
            raise SyntaxError("Expected %r but found %r" % expected_type, token)
        return token
    except IndexError:
        raise SyntaxError("Expected %r" % expected_type)


def parse_identifier(tokens: list[Token]) -> Identifier:
    # tok.type = Token.TokenType.Identifier
    # tok.value == "main"
    # -> Identifier(name="main", parent=None)
    tok = expect_token_type(Token.TokenType.Identifier, tokens)
    return Identifier(parent=None, name=tok.value)


def parse_statement(tokens: list[Token]) -> Statement:
    # chapter 1
    return parse_return_statement(tokens)


def parse_function(tokens: list[Token]) -> FunctionDefinition:
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


def parse_program(tokens: list[Token]):
    parse_function(tokens)
    # no extra junk after function
    # TODO: better!
    assert len(tokens) == 0


def parse(tokens: list[Token]):
    parse_program(tokens)


def parse_expression(tokens: list[Token]) -> Exp:
    # chapter 1, constant only
    tok = expect_token_type(Token.TokenType.Constant, tokens)
    return Constant(None, value=tok.value)


def parse_return_statement(tokens: list) -> Return:
    """Parses a list of tokens representing a return statement and validates the syntax.

    Args:
        tokens: A list of tuples where each tuple consists of a token type and its
                corresponding value.

    Returns:
        AST node representing the Return statement.
    """

    # "return" <exp> ";"
    expect_token_type(Token.TokenType.ReturnKeyword, tokens)
    expr = parse_expression(tokens)
    expect_token_type(Token.TokenType.Semicolon, tokens)

    ret = Return(parent=None)
    expr.parent = ret
    return ret
