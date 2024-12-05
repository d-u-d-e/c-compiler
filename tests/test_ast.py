import unittest

from loguru import logger

from compiler.assembly_generation.assembly_generation import generate_assembly_ast
from compiler.lexer.lexer import Token
from compiler.parser.parser import generate_parse_tree
from lib.ast.ast import generate_pretty_ast_repr

logger.remove()


class TestAstChapter01(unittest.TestCase):
    token_list = [
        Token(Token.TokenType.IntKeyword),
        Token(Token.TokenType.Identifier, "main"),
        Token(Token.TokenType.OpenParenthesis),
        Token(Token.TokenType.VoidKeyword),
        Token(Token.TokenType.CloseParenthesis),
        Token(Token.TokenType.OpenBrace),
        Token(Token.TokenType.ReturnKeyword),
        Token(Token.TokenType.Constant, 100),
        Token(Token.TokenType.Semicolon),
        Token(Token.TokenType.CloseBrace),
    ]
    parse_tree = generate_parse_tree(token_list.copy())
    assembly_tree = generate_assembly_ast(parse_tree)

    def test_generate_pretty_ast_repr_for_parsing(self):
        expected = (
            "Program(\n"
            "   Function(\n"
            "      name=Identifier(main),\n"
            "      body=Return(\n"
            "         Constant(100)\n"
            "      )\n"
            "   )\n"
            ")"
        )
        actual = generate_pretty_ast_repr(self.parse_tree)
        self.assertEqual(expected, actual)

    def test_generate_pretty_ast_repr_for_assembly(self):
        expected = (
            "Program(\n"
            "   Function(\n"
            "      name=Identifier(main),\n"
            "      Mov(\n"
            "         src=Immediate(100),\n"
            "         dst=Register(eax)\n"
            "      ),\n"
            "      Return\n"
            "   )\n"
            ")"
        )
        actual = generate_pretty_ast_repr(self.assembly_tree)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
