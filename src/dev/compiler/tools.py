import re


def clean_comments(lines, delimiter=';'):
    lines = re.sub(r'(\n\s*)+\n+', '\n', lines)

    quotes = '\'"'
    opening_quote = None
    quote_opened = False
    is_comment = False
    cleaned = ''
    line = 1
    for pos, char in enumerate(lines + '\n\n'):  # add some newlines to ensure that bools will be reseted
        if char in quotes:
            if not opening_quote:
                opening_quote = char
                quote_opened = True
            else:
                if opening_quote == char:
                    opening_quote = None
                    quote_opened = False
        elif char == '#' and not quote_opened:
            is_comment = True
            continue
        if is_comment:
            if char == '\n':
                if quote_opened:
                    raise SyntaxError(f'Not closed string on line {line}')
                is_comment = False
                opening_quote = None
                quote_opened = False
                line += 1
            else:
                continue
        cleaned += char

    delimiters = [-1]
    for pos, char in enumerate(cleaned):
        if char in quotes:
            if not opening_quote:
                opening_quote = char
                quote_opened = True
            else:
                if opening_quote == char:
                    opening_quote = None
                    quote_opened = False
        if char == delimiter and not quote_opened:
            delimiters.append(pos)

    if len(delimiters) <= 1:
        return cleaned
    cleaned_lines = list()
    for start, stop in zip(delimiters, delimiters[1:] + [-1]):
        cleaned_line = cleaned[start + 1:stop + 1].strip()
        if not cleaned_line:
            continue
        cleaned_lines.append(cleaned_line.rstrip(delimiter))
    return cleaned_lines
