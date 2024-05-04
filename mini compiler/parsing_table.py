import re
from tabulate import tabulate

# Define tokens with regular expressions
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


# Recursive descent parser 
def recursive_descent_parser(tokens):

    parsing_steps = []

    index = 0
    parse_tree = []

    while index < len(tokens):
        token_type, value, line_number = tokens[index]
        node = []

        if token_type in ['INT', 'FLOAT', 'CHAR']:

            declaration_node = [f"Declaration: {value}"]
            node.append(declaration_node)
            if tokens[index + 1][0] != 'ID':
                raise SyntaxError(f"Expected ID at line {tokens[index + 1][2]}")
            id_node = ['ID:', tokens[index + 1][1]]
            declaration_node.append(id_node)
            if tokens[index + 2][0] != 'ASSIGN':
                raise SyntaxError(f"Expected ASSIGN at line {tokens[index + 2][2]}")
            assignment_node = ['Assignment: =']
            declaration_node.append(assignment_node)
            if tokens[index + 3][0] not in ['NUMBER', 'CHAR_LITERAL']:
                raise SyntaxError(f"Expected NUMBER or CHAR_LITERAL at line {tokens[index + 3][2]}")
            value_node = [tokens[index + 3][0], tokens[index + 3][1]] 
            assignment_node.append(value_node)
            if tokens[index + 4][0] != 'SEMICOLON':
                raise SyntaxError(f"Expected SEMICOLON at line {tokens[index + 4][2]}")
            index += 5 
        else:
            raise SyntaxError(f"Unexpected token {token_type} at line {line_number}")

        parse_tree.append(node)

    return parse_tree


code = '''
int a = 5;
float b = 3.14;
char c = 'A';
char d = 's + 1';
int e = 1;
int f = 100;
'''


code_table = tabulate([[code]], headers=['Code'], tablefmt='grid')

print("\nCode:")
print(code_table)


try:
    parsing_steps = recursive_descent_parser(list(lexer(code)))
    print("\nParsing successful!")

    print("\nParsing table:")
    print(tabulate(parsing_steps, headers=['Step', 'Result'], tablefmt='grid'))

except SyntaxError as e:
    print("\nParsing error:", e)
