import re

# Define token patterns using regular expressions
token_patterns = [
    ('NUMBER', r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('EQUALS', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMICOLON', r';'),
]

# Combine token patterns into a single regular expression
token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_patterns)

# Compile regular expression
token_pattern = re.compile(token_regex)

# Define the parsing table
parsing_table = {
    'program': {
        'IDENTIFIER': ['statement', 'SEMICOLON'],
    },
    'statement': {
        'IDENTIFIER': ['assignment'],
        'LPAREN': ['expr'],
    },
    'assignment': {
        'IDENTIFIER': ['IDENTIFIER', 'EQUALS', 'expr'],
    },
    'expr': {
        'IDENTIFIER': ['term', 'expr_tail'],
        'LPAREN': ['term', 'expr_tail'],
        'NUMBER': ['term', 'expr_tail'],
    },
    'expr_tail': {
        'PLUS': ['PLUS', 'term', 'expr_tail'],
        'MINUS': ['MINUS', 'term', 'expr_tail'],
        'SEMICOLON': [],
        'RPAREN': [],
    },
    'term': {
        'IDENTIFIER': ['factor', 'term_tail'],
        'LPAREN': ['factor', 'term_tail'],
        'NUMBER': ['factor', 'term_tail'],
    },
    'term_tail': {
        'MULTIPLY': ['MULTIPLY', 'factor', 'term_tail'],
        'DIVIDE': ['DIVIDE', 'factor', 'term_tail'],
        'PLUS': [],
        'MINUS': [],
        'SEMICOLON': [],
        'RPAREN': [],
    },
    'factor': {
        'IDENTIFIER': ['IDENTIFIER'],
        'LPAREN': ['LPAREN', 'expr', 'RPAREN'],
        'NUMBER': ['NUMBER'],
    }
}


# Tokenize input text
def tokenize(text):
    for match in token_pattern.finditer(text):
        token_type = match.lastgroup
        token_value = match.group()
        yield token_type, token_value

# Recursive descent parser
def parse(tokens):
    stack = ['program']
    token_stream = iter(tokens)
    token = None

    while stack:
        if token is None:
            token = next(token_stream, None)

        top_of_stack = stack[-1]

        if top_of_stack in parsing_table:
            if token and token[0] in parsing_table[top_of_stack]:
                stack.pop()  # Remove non-terminal from stack
                production = parsing_table[top_of_stack][token[0]]
                stack.extend(reversed(production))  # Push production to stack in reverse order
            else:
                raise SyntaxError(f"Unexpected token '{token[1]}'")
        elif top_of_stack == token[0]:
            stack.pop()  # Remove terminal from stack
            token = None
        else:
            raise SyntaxError(f"Unexpected token '{token[1]}'")

    return True

# Test the parser
def main():
    text = "x = 10 + (y * 5); y = x - 2;"
    tokens = list(tokenize(text))
    print(tokens)
    try:
        result = parse(tokens)
        print("Parsing successful!")
    except SyntaxError as e:
        print("Parsing failed:", e)

if __name__ == "__main__":
    main()
