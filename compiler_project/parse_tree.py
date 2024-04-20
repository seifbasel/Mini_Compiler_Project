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

# Recursive descent parser with parse tree construction
def parse(tokens):
    stack = [('program', [])]
    token_stream = iter(tokens)
    token = None

    while stack:
        if token is None:
            token = next(token_stream, None)

        if token is None:
            break  # No more tokens left, end parsing

        top_of_stack, children = stack[-1]

        if top_of_stack in parsing_table:
            if token[0] in parsing_table[top_of_stack]:
                stack.pop()  # Remove non-terminal from stack
                production = parsing_table[top_of_stack][token[0]]
                production_with_children = [(symbol, []) for symbol in production]
                children.extend(production_with_children)  # Add production to parse tree
                stack.extend(reversed(production_with_children))  # Push production to stack
                token = None  # Consume token
            else:
                raise SyntaxError(f"Unexpected token '{token[1]}'")
        elif top_of_stack == token[0]:
            stack.pop()  # Remove terminal from stack
            children.append(token)
            token = None
        else:
            raise SyntaxError(f"Unexpected token '{token[1]}'")

    return True, stack[0][1]

# Test the parser and print parsing table and tree
def main():
    text = '''x = 10 + (y * 5);
    y = x - 2;'''
    tokens = list(tokenize(text))
    print("Tokens:", tokens)
    try:
        success, parse_tree = parse(tokens)
        print("Parsing successful!")
        print("\nParsing Table:")
        for non_terminal, transitions in parsing_table.items():
            print(non_terminal + ":")
            for terminal, production in transitions.items():
                print(f"  {terminal} -> {' '.join(production)}")

        print("\nParse Tree:")
        print_parse_tree(parse_tree)
    except SyntaxError as e:
        print("Parsing failed:", e)

def print_parse_tree(tree, depth=0):
    for symbol, children in tree:
        if isinstance(symbol, tuple):
            print(" " * depth * 2 + symbol[0])
            print_parse_tree(children, depth + 1)
        else:
            print(" " * depth * 2 + symbol)

if __name__ == "__main__":
    main()
