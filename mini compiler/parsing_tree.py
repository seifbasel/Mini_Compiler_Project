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

# Recursive descent parser function
def recursive_descent_parser(tokens):
    # Initialize a list to store parsing steps and results
    parsing_steps = []

    # Helper function for parsing an expression
    def parse_expression(index):
        token_type, value, line_number = tokens[index]
        node = [f"Expression: {value}"]

        if token_type in ['NUMBER', 'CHAR_LITERAL', 'ID']:
            node.append(value)
            return node, index + 1  # Consume the token and move to the next
        elif token_type == 'LPAREN':
            # Parse the expression inside parentheses
            inner_node, index = parse_expression(index + 1)
            if tokens[index][0] != 'RPAREN':
                raise SyntaxError(f"Expected RPAREN at line {tokens[index][2]}")
            node.append(inner_node)
            return node, index + 1  # Move past the closing parenthesis
        elif token_type == 'PLUS' or token_type == 'MINUS':
            node.append(value)
            inner_node, index = parse_expression(index + 1)  # Parse the next expression
            node.append(inner_node)
            return node, index
        else:
            raise SyntaxError(f"Unexpected token {token_type} at line {line_number}")

    index = 0
    parse_tree = []

    while index < len(tokens):
        token_type, value, line_number = tokens[index]
        node = []

        if token_type == 'INT' or token_type == 'FLOAT' or token_type == 'CHAR':
            # Declaration statement
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
            expr_node, index = parse_expression(index + 3)  # Parse the expression after '='
            assignment_node.append(expr_node)
            if tokens[index][0] != 'SEMICOLON':
                raise SyntaxError(f"Expected SEMICOLON at line {tokens[index][2]}")
            index += 1  # Move past the semicolon
        else:
            raise SyntaxError(f"Unexpected token {token_type} at line {line_number}")

        parse_tree.append(node)

    # Return the parse tree
    return parse_tree

def print_tree(tree, indent=0):
    for node in tree:
        if isinstance(node, list):
            print_tree(node, indent + 2)
        else:
            print(" " * indent + str(node))


# Example usage
code = '''
int a = 5;
float b = 3.14;
char c = 'A';
char d = 's + 1';
int e = 1;
int f = 100;
'''

# Print the code itself
code_table = tabulate([[code]], headers=['Code'], tablefmt='grid')

# Print the tables with titles
print("\nCode:")
print(code_table)


# Parse the code using recursive descent parser
try:
    parse_tree = recursive_descent_parser(list(lexer(code)))
    print("\nParsing successful!")

    # Print the parse tree
    print("\nParse Tree:")
    print_tree(parse_tree)  # Assume print_tree function is defined to print nested lists/dictionaries nicely

except SyntaxError as e:
    print("\nParsing error:", e)