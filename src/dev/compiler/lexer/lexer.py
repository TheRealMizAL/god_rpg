from pathlib import Path

from src.dev.compiler.grammar import Grammar
from src.dev.compiler.tools import clean_comments


class Lexer:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.block_start = Lexem('indent', grammar.block_start)
        self.block_end = Lexem('dedent', grammar.block_end)

        self.all_delimiters = (set(grammar.delimiters) | grammar.operators) | {' '}

    def parse_code(self, path: str | Path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = clean_comments(f.read(), delimiter='\n')
        quotes = '\'"'
        for line in lines:
            lexem = ''
            opening_quote = None
            quote_opened = False
            for i, char in enumerate(line):
                if char in quotes:
                    if not opening_quote:
                        opening_quote = char
                        quote_opened = True
                    else:
                        if opening_quote == char:
                            opening_quote = None
                            quote_opened = False
                lexem += char
                if i == len(line) - 1 or \
                        (line[i + 1] in self.all_delimiters and not quote_opened) \
                        or lexem in self.all_delimiters:
                    lexem = lexem.strip()

                    if lexem:
                        yield self.find_lexem(lexem) or lexem
                    lexem = ''
                    opening_quote = None
                    quote_opened = False

    def find_lexem(self, lexem):
        if lexem in self.grammar.keywords:
            return Lexem('keyword', lexem)
        elif lexem in self.all_delimiters:
            return Lexem('delimiter', lexem)
        elif lexem.isdigit():
            return Lexem('number', lexem)
        elif lexem.startswith('\'') and lexem.endswith('\'') or \
                lexem.startswith('"') and lexem.endswith('"'):
            return Lexem('string', lexem)
        return Lexem('id', lexem)


class Lexem:

    def __init__(self, name: str, definition: str | None):
        self.name = name
        self.definition = definition

    def __repr__(self):
        return f'<Lexem({self.name=}, {self.definition=})>'
