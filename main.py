import re

# Define token types using regular expressions
token_patterns = [
    (r'\bif\b', 'IF'),             # Keyword IF
    (r'\belif\b', 'ELIF'),         # Keyword ELIF
    (r'\belse\b', 'ELSE'),         # Keyword ELSE
    (r'\bfo\b', 'FOR'),           # Keyword FOR
    (r'\bwhi\b', 'WHILE'),       # Keyword WHILE
    (r'\btr\b', 'TRUE'),         # Boolean TRUE
    (r'\bfa\b', 'FALSE'),       # Boolean FALSE
    (r'\ban\b', 'AND'),           # Logical AND
    (r'\bor\b', 'OR'),             # Logical OR
    (r'\bno\b', 'NOT'),           # Logical NOT
    (r'\d+', 'INTEGER'),           # Integer constant
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),  # Identifiers (variable names)
    (r'[-+*/=]', 'OPERATOR'),      # Arithmetic and assignment operators
    (r'[()=]', 'PUNCTUATION'),     # Parentheses and equals sign
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

# Example usage:
source_code = """
x = 5
WHI x < 10 =
    x = x + 1
    IF x > 1=
    x=x+1
"""
tokens = tokenize(source_code)
print(tokens)

