import re
from tabulate import tabulate

# grammer i am using in this mini compiler

# <program>        ::= <declaration>*
# <declaration>    ::= <type> <ID> "=" <value> ";"
# <type>           ::= "int"
# <value>          ::= <NUMBER>


# tokens with regular expressions

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
                    yield (token_type, value, line_number) 
                pos = match.end()
                matched = True
                break
        if not matched:
            raise Exception('Unexpected character: ' + code[pos])


def recursive_descent_parser(tokens):
    index = 0

    def declaration():
        nonlocal index
        if index >= len(tokens):
            return
        token_type, value, line_number = tokens[index]
        node = []

        if token_type in ['INT', 'FLOAT', 'CHAR']:
            # Declaration statement
            declaration_node = [f"Declaration: {value}"]
            node.append(declaration_node)
            index += 1
            if index >= len(tokens) or tokens[index][0] != 'ID':
                raise SyntaxError(f"Expected ID at line {tokens[index][2]}")
            id_node = ['ID:', tokens[index][1]]
            declaration_node.append(id_node)
            index += 1
            if index >= len(tokens) or tokens[index][0] != 'ASSIGN':
                raise SyntaxError(f"Expected ASSIGN at line {tokens[index][2]}")
            assignment_node = ['Assignment: =']
            declaration_node.append(assignment_node)
            index += 1
            if index >= len(tokens) or tokens[index][0] not in ['NUMBER', 'CHAR_LITERAL']:
                raise SyntaxError(f"Expected NUMBER or CHAR_LITERAL at line {tokens[index][2]}")
            value_node = [tokens[index][0], tokens[index][1]]
            assignment_node.append(value_node)
            index += 1
            if index >= len(tokens) or tokens[index][0] != 'SEMICOLON':
                raise SyntaxError(f"Expected SEMICOLON at line {tokens[index][2]}")
            index += 1

        return node

    parse_tree = []

    while index < len(tokens):
        try:
            node = declaration()
            if node:
                parse_tree.extend(node)
            else:
                raise SyntaxError("Unexpected end of input")
        except SyntaxError as e:
            print(e)
            break

    # Return the parse tree
    return parse_tree


def print_tree(tree, indent=0):
    for node in tree:
        if isinstance(node, list):
            print_tree(node, indent + 2)
        else:
            print(" " * indent + str(node))


# Unordered Symbol Table function
def unordered_symbol_table(code):
    symbol_table = {}
    data_type = None
    assignment_mode = True
    object_address_counter = 100  # Initial memory address counter
    for token_type, value, line_number in lexer(code):
        if token_type in ['INT', 'FLOAT', 'CHAR']:
            data_type = value  # Update current data type
            continue
        elif token_type == 'ID':
            identifier = value
            if identifier not in symbol_table:
                # Initialize symbol details if the identifier is not in the table
                symbol_table[identifier] = {
                    'type': data_type,
                    'value': None,
                    'line_declared': line_number,
                    'number_of_dimensions': 0,
                    'signal_lines': {line_number},  # Initialize signal lines with the current line
                    'object_address': object_address_counter
                }
                # Increment object address counter by 2 if data type is 'char'
                if data_type == 'char':
                    object_address_counter += 2
                else:
                    object_address_counter += 1  # Increment object address counter by 1 for other data types
            else:
                # Update signal lines for existing identifier
                symbol_table[identifier]['signal_lines'].add(line_number)
        elif token_type == 'ASSIGN':
            assignment_mode = True  # Enable assignment mode
        elif token_type in ['NUMBER', 'CHAR_LITERAL'] and assignment_mode:
            # Assign value to the identifier if in assignment mode
            symbol_table[identifier]['value'] = value
            assignment_mode = False  # Disable assignment mode after assignment
        elif token_type == 'ID' and not assignment_mode:
            # Update signal lines when the variable is used
            if value in symbol_table:
                symbol_table[value]['signal_lines'].add(line_number)
    return symbol_table

# Example usage
code = '''
int a = 5;
float b = 3.14;
char c = 'A';
char d = 's + 1';
int e = 1;
int f = 555;
int g = 1;
'''

# Get tokens
tokens_table = tabulate(lexer(code), headers=['Token Type', 'Value', 'Line Number'], tablefmt='grid', showindex=False)

# Get symbol table
symbol_table_unordered = unordered_symbol_table(code)
symbol_table_data = [['Variable name', 'Type', 'Value', 'Line Declared', 'Number of Dimensions', 'Signal Lines', 'Object Address']]
for identifier, details in symbol_table_unordered.items():
    symbol_table_data.append([identifier, details['type'], details['value'], details['line_declared'],
                              details['number_of_dimensions'], details['signal_lines'], details['object_address']])
symbol_table = tabulate(symbol_table_data, headers='firstrow', tablefmt='grid')

# Print the code itself
code_table = tabulate([[code]], headers=['Code'], tablefmt='grid')

# Print the tables with titles
print("\nCode:")
print(code_table)
print("Tokens:")
print(tokens_table)
print("\nSymbol Table:")
print(symbol_table)

# Parse the code using recursive descent parser
try:
    parsing_steps = recursive_descent_parser(list(lexer(code)))
    print("\nParsing successful!")

    # Print the parsing steps and results in a table
    print("\nParsing Steps:")
    print(tabulate(parsing_steps, headers=['Step', 'Result'], tablefmt='grid'))

except SyntaxError as e:
    print("\nParsing error:", e)


# Parse the code using recursive descent parser
try:
    parse_tree = recursive_descent_parser(list(lexer(code)))
    print("\nParsing successful!")

    # Print the parse tree
    print("\nParse Tree:")
    print_tree(parse_tree)  # Assume print_tree function is defined to print nested lists/dictionaries nicely

except SyntaxError as e:
    print("\nParsing error:", e)
