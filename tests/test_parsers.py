import unittest

from loguru import logger

from compiler.lexer.lexer import Token
from compiler.parser.ast import (
    Constant,
    FunctionDefinition,
    Identifier,
    Program,
    Return,
    Statement,
)
from compiler.parser.parsers import (
    expect_token_type,
    parse_expression,
    parse_function,
    parse_identifier,
    parse_program,
    parse_return_statement,
    run_parser,
)
from lib.tree.tree import Tree

logger.remove()


class TestParserChapter01(unittest.TestCase):
    valid_return_program_token_list = [
        Token(Token.TokenType.IntKeyword),
        Token(Token.TokenType.Identifier, "main"),
        Token(Token.TokenType.OpenParenthesis),
        Token(Token.TokenType.VoidKeyword),
        Token(Token.TokenType.CloseParenthesis),
        Token(Token.TokenType.OpenBrace),
        Token(Token.TokenType.ReturnKeyword),
        Token(Token.TokenType.Constant, 2),
        Token(Token.TokenType.Semicolon),
        Token(Token.TokenType.CloseBrace),
    ]

    def test_run_valid_token_list(self):
        output = run_parser(self.valid_return_program_token_list.copy())

        self.assertIsInstance(output, Tree)

    def test_parse_program_valid_token_list(self):
        output = parse_program(self.valid_return_program_token_list.copy())

        self.assertIsInstance(output, Program)

    def test_parse_program_child_check(self):
        output = parse_program(self.valid_return_program_token_list.copy())

        self.assertTrue(
            any(isinstance(child, FunctionDefinition) for child in output.children),
            msg="The Program AST node should have a FunctionDefinition node as a child",
        )

    def test_parse_program_list_with_junk(self):
        with self.assertRaises(SyntaxError):
            list_with_junk = self.valid_return_program_token_list.copy()
            list_with_junk.append(Token(Token.TokenType.CloseBrace))
            parse_program(list_with_junk)

    def test_parse_function_valid_token_list(self):
        output = parse_function(self.valid_return_program_token_list.copy())

        self.assertIsInstance(output, FunctionDefinition)
        self.assertIsInstance(output.name, Identifier)
        self.assertIsInstance(output.body, Return)

    def test_parse_function_child_check(self):
        output = parse_function(self.valid_return_program_token_list.copy())

        self.assertTrue(
            any(isinstance(child, Statement) for child in output.children),
            msg="The FunctionDefinition AST node should have a Statement node as a child",
        )

    def test_parse_function_invalid_token_list(self):
        tokens = [
            Token(Token.TokenType.Semicolon),  # Invalid token
            Token(Token.TokenType.Identifier, "main"),
            Token(Token.TokenType.OpenParenthesis),
            Token(Token.TokenType.VoidKeyword),
            Token(Token.TokenType.CloseParenthesis),
            Token(Token.TokenType.OpenBrace),
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.Constant, 2),
            Token(Token.TokenType.Semicolon),
            Token(Token.TokenType.CloseBrace),
        ]

        with self.assertRaises(SyntaxError):
            parse_function(tokens)

    def test_parse_function_invalid_identifier(self):
        tokens = [
            Token(Token.TokenType.IntKeyword),
            Token(Token.TokenType.OpenBrace),  # Invalid identifier
            Token(Token.TokenType.OpenParenthesis),
            Token(Token.TokenType.VoidKeyword),
            Token(Token.TokenType.CloseParenthesis),
            Token(Token.TokenType.OpenBrace),
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.Constant, 2),
            Token(Token.TokenType.Semicolon),
            Token(Token.TokenType.CloseBrace),
        ]

        with self.assertRaises(SyntaxError):
            parse_function(tokens)

    def test_parse_function_invalid_expression(self):
        tokens = [
            Token(Token.TokenType.IntKeyword),
            Token(Token.TokenType.Identifier, "main"),
            Token(Token.TokenType.OpenParenthesis),
            Token(Token.TokenType.VoidKeyword),
            Token(Token.TokenType.CloseParenthesis),
            Token(Token.TokenType.OpenBrace),
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.VoidKeyword),  # Invalid expression
            Token(Token.TokenType.Semicolon),
            Token(Token.TokenType.CloseBrace),
        ]

        with self.assertRaises(SyntaxError):
            parse_function(tokens)

    def test_parse_return_statement_valid_token_list(self):
        tokens = [
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.Constant),
            Token(Token.TokenType.Semicolon),
        ]

        output = parse_return_statement(tokens)

        self.assertIsInstance(output, Return)
        self.assertEqual(output.parent, None)

    def test_parse_return_statement_child_check(self):
        tokens = [
            Token(Token.TokenType.ReturnKeyword),
            Token(Token.TokenType.Constant, 1),
            Token(Token.TokenType.Semicolon),
        ]

        output = parse_return_statement(tokens)

        self.assertTrue(
            any(isinstance(child, Constant) for child in output.children),
            msg="The Return AST node should have a Constant node as a child",
        )

        for child in output.children:
            if isinstance(child, Constant):
                self.assertEqual(child.value, 1)

    def test_parse_return_statement_invalid_token_list(self):
        tokens = [
            Token(Token.TokenType.VoidKeyword),  # Invalid token
            Token(Token.TokenType.Constant),
            Token(Token.TokenType.Semicolon),
        ]

        with self.assertRaises(SyntaxError):
            parse_return_statement(tokens)

    def test_parse_identifier_valid_token_type(self):
        token = Token(Token.TokenType.Identifier, "test_value")
        tokens = [token]

        output = parse_identifier(tokens)

        self.assertIsInstance(output, Identifier)
        self.assertEqual(output.parent, None)
        self.assertEqual(output.name, "test_value")

    def test_parse_identifier_invalid_token_type(self):
        tokens = [Token(Token.TokenType.Constant)]

        with self.assertRaises(SyntaxError):
            parse_identifier(tokens)

    def test_parse_expression_valid_token_type(self):
        token = Token(Token.TokenType.Constant, 1)
        tokens = [token]

        output: Constant = parse_expression(tokens)

        self.assertIsInstance(output, Constant)
        self.assertEqual(output.parent, None)
        self.assertEqual(output.value, 1)

    def test_parse_expression_invalid_token_type(self):
        tokens = [Token(Token.TokenType.Identifier)]

        with self.assertRaises(SyntaxError):
            parse_expression(tokens)

    def test_expect_token_type_valid_token(self):
        tokens = [Token(Token.TokenType.IntKeyword)]

        output = expect_token_type(Token.TokenType.IntKeyword, tokens)

        self.assertIsInstance(output, Token)
        self.assertEqual(output.type, Token.TokenType.IntKeyword)

    def test_expect_token_type_invalid_token(self):
        tokens = [
            Token(Token.TokenType.ReturnKeyword),
        ]

        with self.assertRaises(SyntaxError):
            expect_token_type(Token.TokenType.IntKeyword, tokens)

    def test_expect_token_type_empty_list(self):
        with self.assertRaises(SyntaxError):
            expect_token_type(Token.TokenType.IntKeyword, [])


if __name__ == "__main__":
    unittest.main()
