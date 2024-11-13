from compiler.ast.parser.ast import Constant, Identifier, Return
from compiler.lexer import Token


def parse_return_statement(tokens: list) -> Return:
    """Parses a list of tokens representing a return statement and validates the syntax.

    Args:
        tokens: A list of tuples where each tuple consists of a token type and its
                corresponding value.

    Returns:
        AST node representing the Return statement.
    """
    return_token_type = tokens.pop(0)[0]
    if return_token_type is not Token.TokenType.ReturnKeyword:
        raise SyntaxError(f"Found {return_token_type} instead of the 'return' keyword.")

    expression = tokens.pop(0)
    exp_type = expression[0]
    exp_value = expression[1]

    if exp_type not in [Token.TokenType.Constant, Token.TokenType.Identifier]:
        raise SyntaxError(f"Found {exp_type} instead of an exp AST node type.")

    semicolon = tokens.pop(0)
    if semicolon is not Token.TokenType.Semicolon:
        raise SyntaxError(f"Found {semicolon} instead of a semicolon.")

    # Create the Exp AST node
    if exp_type == Token.TokenType.Constant:
        exp_ast_node = Constant(value=exp_value)
    elif exp_type == Token.TokenType.Identifier:
        exp_ast_node = Identifier(value=exp_value)

    # TODO: Should we assign the parent to the return AST node here?
    return Return(parent=None, value=exp_ast_node)
