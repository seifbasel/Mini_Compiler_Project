import re
from tabulate import tabulate

tokens = [
    ('NUMBER', r'\d+(\.\d+)?'),   
    ('ASSIGN', r'\='),
    ('INT', r'int'),
    ('FLOAT', r'float'),
    ('CHAR', r'char'),
    ('CHAR_LITERAL', r"\'[^\']*\'"), 
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  
    ('SEMICOLON', r'\;'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
]

# Lexer 
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
                    yield (token_type, value, line_number)  
                pos = match.end()
                matched = True
                break
        if not matched:
            raise Exception('Unexpected character: ' + code[pos])

# test code
code = '''
int a = 5;
float b = 3.14;
char c = 'A';
char d = 's + 1';
int e = 1;
int f = 100;
'''

# Get the tokens
tokens_table = tabulate(lexer(code), headers=['Token Type', 'Value', 'Line Number'], tablefmt='grid')

# Print the test code 
code_table = tabulate([[code]], headers=['Code'], tablefmt='grid')

# Print the tables
print("\nCode:")
print(code_table)
print("Tokens:")
print(tokens_table)
