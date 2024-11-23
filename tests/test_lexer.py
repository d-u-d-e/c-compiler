import os
import subprocess
import unittest
from tempfile import NamedTemporaryFile

from loguru import logger

import compiler.lexer.lexer as lexer
from compiler.compiler_driver import gcc_preprocess
from compiler.lexer.lexer import Token

logger.remove()


class TestLexerChapter01(unittest.TestCase):
    test_samples_path = "tests/test_samples/chapter_1"

    def test_multi_digit(self):
        path = os.path.join(self.test_samples_path, "valid", "multi_digit.c")
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

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            tokens = [
                (token.type, token.value)
                for token in lexer.run_lexer(preprocessed_file.name)
            ]

        self.assertListEqual(tokens, expected_list)

    def test_newlines(self):
        path = os.path.join(self.test_samples_path, "valid", "newlines.c")
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

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            tokens = [
                (token.type, token.value)
                for token in lexer.run_lexer(preprocessed_file.name)
            ]

        self.assertListEqual(tokens, expected_list)

    def test_no_newlines(self):
        path = os.path.join(self.test_samples_path, "valid", "no_newlines.c")
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

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            try:
                gcc_preprocess(path, preprocessed_file.name)
            except subprocess.CalledProcessError as e:
                return e.returncode

            tokens = lexer.run_lexer(preprocessed_file.name)

        for i in range(len(tokens)):
            tokens[i] = (tokens[i].type, tokens[i].value)

        self.assertListEqual(tokens, expected_list)

    def test_return_int(self):
        path = os.path.join(self.test_samples_path, "valid", "return_2.c")
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

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            tokens = [
                (token.type, token.value)
                for token in lexer.run_lexer(preprocessed_file.name)
            ]

        self.assertListEqual(tokens, expected_list)

    def test_spaces(self):
        path = os.path.join(self.test_samples_path, "valid", "spaces.c")
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

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            tokens = [
                (token.type, token.value)
                for token in lexer.run_lexer(preprocessed_file.name)
            ]

        self.assertListEqual(tokens, expected_list)

    def test_tabs(self):
        path = os.path.join(self.test_samples_path, "valid", "tabs.c")
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

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            tokens = [
                (token.type, token.value)
                for token in lexer.run_lexer(preprocessed_file.name)
            ]

        self.assertListEqual(tokens, expected_list)

    def test_at_sign(self):
        path = os.path.join(self.test_samples_path, "invalid_lex", "at_sign.c")

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            with self.assertRaises(ValueError):
                lexer.run_lexer(preprocessed_file.name)

    def test_backslash(self):
        path = os.path.join(self.test_samples_path, "invalid_lex", "backslash.c")

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            with self.assertRaises(ValueError):
                lexer.run_lexer(preprocessed_file.name)

    def test_backtick(self):
        path = os.path.join(self.test_samples_path, "invalid_lex", "backtick.c")

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            with self.assertRaises(ValueError):
                lexer.run_lexer(preprocessed_file.name)

    def test_invalid_identifier_2(self):
        path = os.path.join(
            self.test_samples_path, "invalid_lex", "invalid_identifier_2.c"
        )

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            with self.assertRaises(ValueError):
                lexer.run_lexer(preprocessed_file.name)

    def test_invalid_identifier(self):
        path = os.path.join(
            self.test_samples_path, "invalid_lex", "invalid_identifier.c"
        )

        with NamedTemporaryFile(suffix=".i") as preprocessed_file:
            gcc_preprocess(path, preprocessed_file.name)
            with self.assertRaises(ValueError):
                lexer.run_lexer(preprocessed_file.name)


if __name__ == "__main__":
    unittest.main()
