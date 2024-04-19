import re
from tabulate import tabulate

# Define tokens
tokens = [
    ('NUMBER', r'\d+(\.\d+)?'),  # Pattern for integers and floats
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'\/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('ASSIGN', r'\='),
    ('INT', r'int'),
    ('FLOAT', r'float'),
    ('CHAR', r'char'),
    ('CHAR_LITERAL', r'\'[^\']*\''),  # Pattern for character literals
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SEMICOLON', r'\;'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
]

# Lexer function
def lexer(code):
    pos = 0
    line_number = 1
    declared_identifiers = set()  # Keep track of declared identifiers
    current_scope = None  # Current scope
    while pos < len(code):
        matched = False
        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':
                    if token_type == 'NEWLINE':
                        line_number += 1
                    elif token_type == 'ID':
                        identifier = value
                        if identifier in declared_identifiers and current_scope == identifier:
                            raise Exception(f"Identifier '{identifier}' already defined")
                        declared_identifiers.add(identifier)
                        yield (token_type, value, line_number)
                    elif token_type == 'LPAREN':
                        current_scope = None  # Start of a new scope
                    elif token_type == 'RPAREN':
                        current_scope = None  # End of the current scope
                    else:
                        yield (token_type, value, None)  # No line number for other tokens
                pos = match.end()
                matched = True
                break
        if not matched:
            raise Exception('Unexpected character: ' + code[pos])

# Unordered Symbol Table function
def unordered_symbol_table(code):
    symbol_table = {}
    data_type = None
    assignment_mode = False
    current_line = 1  # Track current line number
    for token_type, value, line_number in lexer(code):
        if token_type in ['INT', 'FLOAT', 'CHAR']:
            data_type = value
            continue
        elif token_type == 'ID':
            identifier = value
            if identifier not in symbol_table:
                symbol_table[identifier] = {
                    'type': data_type,
                    'value': None,
                    'line_declared': line_number,
                    'number_of_dimensions': 0,
                    'signal_lines': {line_number},  # Initialize signal_lines with the current line
                    'object_address': None
                }
            else:
                symbol_table[identifier]['signal_lines'].add(line_number)  # Update signal_lines for existing identifier
        elif token_type == 'ASSIGN':
            assignment_mode = True
        elif token_type in ['NUMBER', 'CHAR_LITERAL'] and assignment_mode:
            symbol_table[identifier]['value'] = value
            assignment_mode = False
        elif token_type == 'ID' and not assignment_mode:
            if value in symbol_table:
                symbol_table[value]['signal_lines'].add(line_number)  # Update signal_lines when variable is used
        elif token_type == 'LBRACKET':  # Track array dimensions
            symbol_table[identifier]['number_of_dimensions'] += 1
        elif token_type == 'RBRACKET':
            pass  # Handle end of array dimension
    return symbol_table



# Example usage
code = '''
int x = 5;
float y = 3.14;
char c = 'A';
float z = x + 1;
'''

symbol_table_unordered = unordered_symbol_table(code)

# Assigning object addresses
object_address_counter = 100  # Initial memory address counter
for identifier, details in symbol_table_unordered.items():
    details['object_address'] = object_address_counter
    object_address_counter += 1

# Converting symbol table to list of lists for tabulate
table_data = [['Variable name', 'Type', 'Value', 'Line Declared', 'Number of Dimensions', 'Signal Lines', 'Object Address']]
for identifier, details in symbol_table_unordered.items():
    table_data.append([identifier, details['type'], details['value'], details['line_declared'],
                       details['number_of_dimensions'], details['signal_lines'], details['object_address']])

# Print table
print(tabulate(table_data, headers='firstrow', tablefmt='grid'))
