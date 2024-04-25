import re
from tabulate import tabulate

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
        elif token_type == 'LBRACKET':  # Track array dimensions
            symbol_table[identifier]['number_of_dimensions'] += 1
        elif token_type == 'RBRACKET':
            pass  # Handle end of array dimension
    return symbol_table
# Example usage
code = '''
int a = 5;
float b = 3.14;
char c = 'A';
char d = 's + 1';
int e = 1;
int f = 100;
'''

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

print("\nSymbol Table:")
print(symbol_table)
