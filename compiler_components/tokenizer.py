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

# Test the lexer
text = "x = 10 + (y * 5); y = x - 2;"
for match in token_pattern.finditer(text):
    print(match.lastgroup, ":", match.group())
