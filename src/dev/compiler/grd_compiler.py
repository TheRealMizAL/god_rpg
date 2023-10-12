from .grammar import Grammar
from .lexer import Lexer


class Compiler:

    def __init__(self, grammar_path):
        self.grammar = Grammar().build_grammar_from_file(grammar_path)
        self.lexer = Lexer()
