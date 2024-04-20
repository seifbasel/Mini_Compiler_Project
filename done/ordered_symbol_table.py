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

# Ordered Symbol Table function
def ordered_symbol_table(code):
    symbol_table = {}
    data_type = None
    declaration_count = 0  # Initialize declaration count
    assignment_mode = False
    object_address_counter = 100  # Initial memory address counter
    for token_type, value, line_number in lexer(code):
        if token_type in ['INT', 'FLOAT', 'CHAR']:
            data_type = value
            continue
        elif token_type == 'ID':
            identifier = value
            if identifier not in symbol_table:
                declaration_count += 1  # Increment declaration count for each new identifier
                symbol_table[identifier] = {
                    'type': data_type,
                    'value': None,
                    'line_declared': line_number,
                    'count': declaration_count,  # Assign the current declaration count
                    'object_address': object_address_counter,  # Assign the current object address
                    'number_of_dimensions': 0  # Number of dimensions for arrays
                }
                object_address_counter += 1  # Increment memory address counter
        elif token_type == 'ASSIGN':
            assignment_mode = True
        elif token_type in ['NUMBER', 'CHAR_LITERAL'] and assignment_mode:
            symbol_table[identifier]['value'] = value
            assignment_mode = False
        elif token_type == 'SEMICOLON':
            data_type = None
    return symbol_table

# Example usage
code = '''int x = 5;
float y = 3.14;
char c = 'A';
float z =5;
'''

symbol_table = ordered_symbol_table(code)

# Converting symbol table to list of lists for tabulate
table_data = [['Count', 'Variable Name', 'Type', 'Value', 'Line Declared', 'Object Address']]
for identifier, details in symbol_table.items():
    table_data.append([details['count'], identifier, details['type'], details['value'],
                       details['line_declared'], details['object_address']])

# Print table
print(tabulate(table_data, headers='firstrow', tablefmt='grid'))
