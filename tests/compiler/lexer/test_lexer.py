import os
import unittest

from loguru import logger

from compiler.lexer.lexer import Token
import compiler.lexer.lexer as lexer

# Disable all log messages
logger.remove()


class TestLexerChapter01(unittest.TestCase):
    relative_path = "tests/compiler/lexer/test_samples/chapter01"

    def test_multi_digit(self):
        path = os.path.join(f"{self.relative_path}/multi_digit.c")
        actual_list = lexer.run(path)
        for i in range(len(actual_list)):
            actual_list[i] = (actual_list[i].type, actual_list[i].value)
        expected_list = [
            (Token.TokenType.IntKeyword, "int"),
            (Token.TokenType.Identifier, "main"),
            (Token.TokenType.OpenParenthesis, "("),
            (Token.TokenType.VoidKeyword, "void"),
            (Token.TokenType.CloseParenthesis, ")"),
            (Token.TokenType.OpenBrace, "{"),
            (Token.TokenType.ReturnKeyword, "return"),
            (Token.TokenType.Constant, "100"),
            (Token.TokenType.Semicolon, ";"),
            (Token.TokenType.CloseBrace, "}"),
        ]

        self.assertListEqual(actual_list, expected_list)

    def test_newlines(self):
        path = os.path.join(f"{self.relative_path}/newlines.c")
        actual_list = lexer.run(path)
        for i in range(len(actual_list)):
            actual_list[i] = (actual_list[i].type, actual_list[i].value)
        expected_list = [
            (Token.TokenType.IntKeyword, "int"),
            (Token.TokenType.Identifier, "main"),
            (Token.TokenType.OpenParenthesis, "("),
            (Token.TokenType.VoidKeyword, "void"),
            (Token.TokenType.CloseParenthesis, ")"),
            (Token.TokenType.OpenBrace, "{"),
            (Token.TokenType.ReturnKeyword, "return"),
            (Token.TokenType.Constant, "0"),
            (Token.TokenType.Semicolon, ";"),
            (Token.TokenType.CloseBrace, "}"),
        ]
        self.assertListEqual(actual_list, expected_list)

    def test_no_newlines(self):
        path = os.path.join(f"{self.relative_path}/no_newlines.c")
        actual_list = lexer.run(path)
        for i in range(len(actual_list)):
            actual_list[i] = (actual_list[i].type, actual_list[i].value)
        expected_list = [
            (Token.TokenType.IntKeyword, "int"),
            (Token.TokenType.Identifier, "main"),
            (Token.TokenType.OpenParenthesis, "("),
            (Token.TokenType.VoidKeyword, "void"),
            (Token.TokenType.CloseParenthesis, ")"),
            (Token.TokenType.OpenBrace, "{"),
            (Token.TokenType.ReturnKeyword, "return"),
            (Token.TokenType.Constant, "0"),
            (Token.TokenType.Semicolon, ";"),
            (Token.TokenType.CloseBrace, "}"),
        ]
        self.assertListEqual(actual_list, expected_list)

    def test_return_int(self):
        path = os.path.join(f"{self.relative_path}/return_2.c")
        actual_list = lexer.run(path)
        for i in range(len(actual_list)):
            actual_list[i] = (actual_list[i].type, actual_list[i].value)
        expected_list = [
            (Token.TokenType.IntKeyword, "int"),
            (Token.TokenType.Identifier, "main"),
            (Token.TokenType.OpenParenthesis, "("),
            (Token.TokenType.VoidKeyword, "void"),
            (Token.TokenType.CloseParenthesis, ")"),
            (Token.TokenType.OpenBrace, "{"),
            (Token.TokenType.ReturnKeyword, "return"),
            (Token.TokenType.Constant, "2"),
            (Token.TokenType.Semicolon, ";"),
            (Token.TokenType.CloseBrace, "}"),
        ]
        self.assertListEqual(actual_list, expected_list)

    def test_spaces(self):
        path = os.path.join(f"{self.relative_path}/spaces.c")
        actual_list = lexer.run(path)
        for i in range(len(actual_list)):
            actual_list[i] = (actual_list[i].type, actual_list[i].value)
        expected_list = [
            (Token.TokenType.IntKeyword, "int"),
            (Token.TokenType.Identifier, "main"),
            (Token.TokenType.OpenParenthesis, "("),
            (Token.TokenType.VoidKeyword, "void"),
            (Token.TokenType.CloseParenthesis, ")"),
            (Token.TokenType.OpenBrace, "{"),
            (Token.TokenType.ReturnKeyword, "return"),
            (Token.TokenType.Constant, "0"),
            (Token.TokenType.Semicolon, ";"),
            (Token.TokenType.CloseBrace, "}"),
        ]
        self.assertListEqual(actual_list, expected_list)

    def test_tabs(self):
        path = os.path.join(f"{self.relative_path}/tabs.c")
        actual_list = lexer.run(path)
        for i in range(len(actual_list)):
            actual_list[i] = (actual_list[i].type, actual_list[i].value)
        expected_list = [
            (Token.TokenType.IntKeyword, "int"),
            (Token.TokenType.Identifier, "main"),
            (Token.TokenType.OpenParenthesis, "("),
            (Token.TokenType.VoidKeyword, "void"),
            (Token.TokenType.CloseParenthesis, ")"),
            (Token.TokenType.OpenBrace, "{"),
            (Token.TokenType.ReturnKeyword, "return"),
            (Token.TokenType.Constant, "0"),
            (Token.TokenType.Semicolon, ";"),
            (Token.TokenType.CloseBrace, "}"),
        ]
        self.assertListEqual(actual_list, expected_list)


if __name__ == "__main__":
    unittest.main()
