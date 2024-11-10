import os
import unittest
from compiler import lexer
from compiler.lexer import Token


class TestLexerChapter01(unittest.TestCase):
    def test_spaces(self):
        path = os.path.join(
            os.path.dirname(__file__), "test_samples/valid/chapter01/spaces.c"
        )
        actual_list = lexer.run(path)
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
