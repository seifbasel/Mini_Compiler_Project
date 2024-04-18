import re

# Define token types using regular expressions
token_patterns = [
    (r'\bif\b', 'IF'),             # Keyword IF
    (r'\belif\b', 'ELIF'),         # Keyword ELIF
    (r'\bwhile\b', 'WHILE'),       # Keyword WHILE
    (r'\d+', 'INTEGER'),           # Integer constant
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),  # Identifiers (variable names)
    (r'[-+*/=]', 'OPERATOR'),      # Arithmetic and assignment operators
    (r'[()=:]', 'PUNCTUATION'),    # Parentheses and equals sign
    (r'==|!=|<=|>=|[<>]=?', 'COMPARISON'),  # Comparison operators
    (r';', 'SEMICOLON'),           # Semicolon
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

#recursive descent parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def match(self, expected_token_type):
        if self.current_token_index < len(self.tokens):
            token_type, _ = self.tokens[self.current_token_index]
            if token_type == expected_token_type:
                self.current_token_index += 1
                return True
        return False

    def parse_expression(self):
        # For simplicity, let's assume an expression is just an identifier followed by an assignment operator and an integer constant
        if self.match('IDENTIFIER') and self.match('OPERATOR') and self.match('INTEGER'):
            return True
        return False

    def parse_statement(self):
        # For simplicity, let's assume a statement is just an expression followed by a semicolon
        if self.parse_expression() and self.match('SEMICOLON'):
            return True
        return False

    def parse(self):
        while self.current_token_index < len(self.tokens):
            if not self.parse_statement():
                raise Exception("Syntax error")
        print("Parsing completed successfully")

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, value):
        self.symbols[name] = value

    def get_value(self, name):
        return self.symbols.get(name, None)

    def print_table(self):
        print("Symbol Table:")
        self._print_tree_structure(self.symbols, 0)

    def _print_tree_structure(self, symbols, level):
        for name, value in symbols.items():
            print("  " * level + f"{name}: {value}")
            if isinstance(value, dict):
                self._print_tree_structure(value, level + 1)

code = """
x = 5;
y = 10;
z = 100;
"""

tokens = tokenize(code)
parser = Parser(tokens)
parser.parse()

symbol_table = SymbolTable()
symbol_table.add_symbol("x", 5)
symbol_table.add_symbol("y", 10)
symbol_table.add_symbol("z", 100)
symbol_table.print_table()