import re
from tabulate import tabulate

# # Define the parse table
# parse_table = {
#     ("<program>", "INT"): ["<declaration_list>"],
#     ("<program>", "FLOAT"): ["<declaration_list>"],
#     ("<program>", "CHAR"): ["<declaration_list>"],
#     ("<declaration_list>", "INT"): ["<declaration>", "<declaration_list>"],
#     ("<declaration_list>", "FLOAT"): ["<declaration>", "<declaration_list>"],
#     ("<declaration_list>", "CHAR"): ["<declaration>", "<declaration_list>"],
#     ("<declaration>", "INT"): ["int", "<ID>", "=", "<value>", ";"],
#     ("<declaration>", "FLOAT"): ["float", "<ID>", "=", "<value>", ";"],
#     ("<declaration>", "CHAR"): ["char", "<ID>", "=", "<value>", ";"],
#     ("<value>", "NUMBER"): ["<NUMBER>"],
#     ("<value>", "CHAR_LITERAL"): ["<CHAR_LITERAL>"],
#     ("<value>", "ID"): ["<ID>"],
#     ("<value>", "LPAREN"): ["(", "<expression>", ")"],
#     ("<expression>", "NUMBER"): ["<value>"],
#     ("<expression>", "CHAR_LITERAL"): ["<value>"],
#     ("<expression>", "ID"): ["<value>"],
#     ("<expression>", "LPAREN"): ["(", "<expression>", ")"],
#     ("<expression>", "PLUS"): ["<expression>", "+", "<expression>"],
#     ("<expression>", "MINUS"): ["<expression>", "-", "<expression>"]
# }

# Define tokens with regular expressions
tokens = [
    ('NUMBER', r'\d+(\.\d+)?'),    # Integer and float numbers
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('ASSIGN', r'\='),
    ('INT', r'int'),
    ('FLOAT', r'float'),
    ('CHAR', r'char'),
    ('CHAR_LITERAL', r"\'[^\']*\'"),  # Character literals
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers (variable names)
    ('SEMICOLON', r'\;'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
]

# Lexer function
def lexer(code):
    pos = 0
    line_number = 1
    while pos < len(code):
        matched = False
        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type == 'NEWLINE':
                    line_number += 1
                elif token_type != 'WHITESPACE':
                    yield (token_type, value, line_number)  # Yield the token
                pos = match.end()
                matched = True
                break
        if not matched:
            raise Exception('Unexpected character: ' + code[pos])

# Example usage
code = '''
int a = 5;
float b = 3.14;
char c = 'A';
char d = 's + 1';
int e = 1;
int f = 100;
'''

# Get tokens
tokens_table = tabulate(lexer(code), headers=['Token Type', 'Value', 'Line Number'], tablefmt='grid', showindex=False)

# Print the code itself
code_table = tabulate([[code]], headers=['Code'], tablefmt='grid')

# Print the tables with titles
print("\nCode:")
print(code_table)
print("Tokens:")
print(tokens_table)
