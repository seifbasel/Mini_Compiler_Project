import re

# Define tokens
tokens = [
    ('NUMBER', r'\d+(\.\d+)?'),  # Pattern for integers and floats
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'\/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('ASSIGN', r'\='),
    ('INT', r'int'),
    ('FLOAT', r'float'),
    ('CHAR', r'char'),
    ('CHAR_LITERAL', r'\'[^\']*\''),  # Pattern for character literals
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SEMICOLON', r'\;'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
]

# Lexer function
def lexer(code):
    pos = 0
    while pos < len(code):
        matched = False
        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':
                    yield (token_type, value)
                pos = match.end()
                matched = True
                break
        if not matched:
            raise Exception('Unexpected character: ' + code[pos])

# Example usage
code = '''
int x = 5;
float y = 3.14;
char c = \'A\';
result = x + y;
'''
for token in lexer(code):
    print(token)

