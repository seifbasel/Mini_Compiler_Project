import re

# Define token types using regular expressions
token_patterns = [
    (r'\bif\b', 'IF'),             # Keyword IF
    (r'\belif\b', 'ELIF'),         # Keyword ELIF
    (r'\bwhile\b', 'WHILE'),       # Keyword WHILE
    (r'\d+', 'INTEGER'),           # Integer constant
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),  # Identifiers (variable names)
    (r'[-+*/=]', 'OPERATOR'),      # Arithmetic and assignment operators
    (r'[()=:]', 'PUNCTUATION'),     # Parentheses and equals sign
    (r'==|!=|<=|>=|[<>]=?', 'COMPARISON'),  # Comparison operators
    (r'\s+', None)                 # Skip whitespace
]

def tokenize(code):
    tokens = []
    pos = 0

    while pos < len(code):
        match = None
        for pattern, token_type in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                if token_type:
                    token_value = match.group(0)
                    tokens.append((token_type, token_value))
                break

        if not match:
            raise Exception(f"Invalid token at position {pos}")

        pos = match.end()

    return tokens


code = """
if x == 5:
    y = 10
elif x < 5:
    y = 5
else:
    y = 0
"""

tokens = tokenize(code)

for token in tokens:
    print(token)
