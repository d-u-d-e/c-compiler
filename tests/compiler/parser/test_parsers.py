import unittest

from loguru import logger

from compiler.lexer.lexer import Token
from compiler.parser.ast import Identifier
from compiler.parser.parsers import parse_identifier

# Disable all log messages
logger.remove()


class TestParserChapter01(unittest.TestCase):
    def test_parse_identifier_valid_token_list(self):
        # Simulate a list of tokens
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

    def test_parse_identifier_not_valid_token_list(self):
        # Simulate a wrong list of tokens
        token = Token(Token.TokenType.Constant)
        token.value = "test"
        tokens = [token]

        with self.assertRaises(SyntaxError):
            parse_identifier(tokens)


if __name__ == "__main__":
    unittest.main()
