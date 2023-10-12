import re
from pathlib import Path

from src.dev.compiler.tools import clean_comments


class Grammar:

    def __init__(self,
                 digit: str | None = None,
                 letter: str | None = None,
                 delimiters: str | None = None,
                 block_start: str | None = None,
                 block_end: str | None = None):
        self.digit = digit or r'[0-9]'
        self.letter = letter or r'[a-zA-Z]'
        self.delimiters = delimiters or r'[,:()]'

        self.block_start = block_start or 'indent'
        self.block_end = block_end or 'dedent'

        self.keywords = set()
        self.operators = set()

        self.rules: list["GrammarRule"] = []

    def build_grammar_from_file(self, grammar_path: str | Path):
        with open(grammar_path, 'r', encoding='utf-8') as gr:
            grammar_lines = bytes(gr.read().encode('utf-8')).decode('unicode_escape')
        cleaned = clean_comments(grammar_lines)
        self.rules = self.__strings_to_dict(cleaned)

        return self

    def __strings_to_dict(self, lines: list[str], sep: str = ':'):
        final = dict()
        for line in lines:
            k, v = line.split(sep, 1)
            if k in final.keys():
                raise KeyError(f'Key {k} already presented')
            open_br = '({['
            close_br = ')}]'
            stack = []
            definition = ''
            for char in v.strip():
                if char in open_br:
                    stack.append(char)
                    if char == '[':
                        definition += '(?:'
                        continue
                    elif char == '{':
                        definition += '('
                        continue
                elif char in close_br:
                    pos = close_br.index(char)
                    if stack and stack[-1] == open_br[pos]:
                        stack.pop()
                    else:
                        raise SyntaxError(f'Wrong braces in rule "{k}"')
                    if char == ']':
                        definition += ')?'
                        continue
                    elif char == '}':
                        definition += ')*'
                        continue

                definition += char
            if stack:
                raise SyntaxError(f'Wrong braces in rule "{k}"')
            final[k] = GrammarRule(k, definition)
        for k, v in final.items():
            self.keywords |= set(keyword.strip('\'') for keyword in re.findall(r'\'(?!_)\w+\'', v.definition))
            self.operators |= set(
                keyword.strip('\'') for keyword in re.findall(r'\'[<>=/*?:+\-%~|^&!,]+\'', v.definition))

        return final


class GrammarRule:
    def __init__(self, name: str, definition: str):
        self.name = name
        self.definition = definition

    def __repr__(self):
        return f'<GrammarRule({self.name} = {self.definition})>'


if __name__ == '__main__':
    grammar = Grammar()
