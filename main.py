import re

# Define token types using regular expressions
token_patterns = [
    (r'\bIF\b', 'IF'),             # Keyword IF
    (r'\bELIF\b', 'ELIF'),         # Keyword ELIF
    (r'\bELSE\b', 'ELSE'),         # Keyword ELSE
    (r'\bFO\b', 'FOR'),           # Keyword FOR
    (r'\bWHI\b', 'WHILE'),       # Keyword WHILE
    (r'\bTR\b', 'TRUE'),         # Boolean TRUE
    (r'\bFA\b', 'FALSE'),       # Boolean FALSE
    (r'\bAN\b', 'AND'),           # Logical AND
    (r'\bOR\b', 'OR'),             # Logical OR
    (r'\bNO\b', 'NOT'),           # Logical NOT
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
