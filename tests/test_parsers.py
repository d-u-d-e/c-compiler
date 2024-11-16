import unittest

from loguru import logger

from compiler.lexer.lexer import Token
from compiler.parser.ast import Constant, Identifier, Return
from compiler.parser.parsers import (
    parse_identifier,
    parse_return_statement,
)

logger.remove()


class TestParserChapter01(unittest.TestCase):
    def test_parse_valid_identifier(self):
        # Simulate a valid list of tokens
        token = Token(Token.TokenType.Identifier)
        token.value = "test"
        tokens = [token]

        # Generate output of the function
        actual_ast_node = parse_identifier(tokens)
        # Expected output AST node
        expected_ast_node = Identifier(parent=None, name=token.value)

        self.assertIsInstance(actual_ast_node, Identifier)
        self.assertEqual(actual_ast_node.name, expected_ast_node.name)
        self.assertEqual(actual_ast_node.parent, expected_ast_node.parent)

    def test_parse_invalid_identifier(self):
        token = Token(Token.TokenType.Constant)  # Invalid token type
        token.value = "test"
        tokens = [token]

        with self.assertRaises(SyntaxError):
            parse_identifier(tokens)

    def test_parse_valid_return_statement(self):
        tokens = [
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.Constant),
            Token(Token.TokenType.Semicolon),
        ]

        actual_ast_node = parse_return_statement(tokens)
        expected_ast_node = Return(parent=None)

        self.assertIsInstance(actual_ast_node, Return)
        self.assertEqual(actual_ast_node.parent, expected_ast_node.parent)

    def test_parse_valid_return_statement_child(self):
        const_ast_node = Token(Token.TokenType.Constant)
        const_ast_node.value = 1
        tokens = [
            Token(Token.TokenType.ReturnKeyword),
            const_ast_node,
            Token(Token.TokenType.Semicolon),
        ]

        actual_ast_node = parse_return_statement(tokens)

        # Assert that the Return node has the Constant node as a child
        self.assertTrue(
            any(isinstance(child, Constant) for child in actual_ast_node.children)
        )

    def test_parse_invalid_return_statement_return_token(self):
        tokens = [
            Token(Token.TokenType.VoidKeyword),  # Invalid token
            Token(Token.TokenType.IntKeyword),
            Token(Token.TokenType.Semicolon),
        ]

        with self.assertRaises(SyntaxError):
            parse_return_statement(tokens)

    def test_parse_invalid_return_statement_exp_token(self):
        tokens = [
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.IntKeyword),  # Invalid token
            Token(Token.TokenType.Semicolon),
        ]

        with self.assertRaises(SyntaxError):
            parse_return_statement(tokens)

    def test_parse_invalid_return_statement_semicolon_token(self):
        tokens = [
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.Constant),
            Token(Token.TokenType.OpenBrace),  # Invalid token
        ]

        with self.assertRaises(SyntaxError):
            parse_return_statement(tokens)


if __name__ == "__main__":
    unittest.main()
