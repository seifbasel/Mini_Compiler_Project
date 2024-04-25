import re
from tabulate import tabulate

# Define the parse table
parse_table = {
    ("<program>", "INT"): ["<declaration_list>"],
    ("<program>", "FLOAT"): ["<declaration_list>"],
    ("<program>", "CHAR"): ["<declaration_list>"],
    ("<declaration_list>", "INT"): ["<declaration>", "<declaration_list>"],
    ("<declaration_list>", "FLOAT"): ["<declaration>", "<declaration_list>"],
    ("<declaration_list>", "CHAR"): ["<declaration>", "<declaration_list>"],
    ("<declaration>", "INT"): ["int", "<ID>", "=", "<value>", ";"],
    ("<declaration>", "FLOAT"): ["float", "<ID>", "=", "<value>", ";"],
    ("<declaration>", "CHAR"): ["char", "<ID>", "=", "<value>", ";"],
    ("<value>", "NUMBER"): ["<NUMBER>"],
    ("<value>", "CHAR_LITERAL"): ["<CHAR_LITERAL>"],
    ("<value>", "ID"): ["<ID>"],
    ("<value>", "LPAREN"): ["(", "<expression>", ")"],
    ("<expression>", "NUMBER"): ["<value>"],
    ("<expression>", "CHAR_LITERAL"): ["<value>"],
    ("<expression>", "ID"): ["<value>"],
    ("<expression>", "LPAREN"): ["(", "<expression>", ")"],
    ("<expression>", "PLUS"): ["<expression>", "+", "<expression>"],
    ("<expression>", "MINUS"): ["<expression>", "-", "<expression>"]
}

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

def recursive_descent_parser(tokens):
    # Initialize a list to store parsing steps and results
    parsing_steps = []

    # Helper function for parsing an expression
    def parse_expression(index):
        token_type, value, line_number = tokens[index]
        parsing_steps.append((f"Parsing expression at line {line_number}", f"{value}"))

        if token_type in ['NUMBER', 'CHAR_LITERAL', 'ID']:
            return index + 1  # Consume the token and move to the next
        elif token_type == 'LPAREN':
            # Parse the expression inside parentheses
            index = parse_expression(index + 1)
            if tokens[index][0] != 'RPAREN':
                raise SyntaxError(f"Expected RPAREN at line {tokens[index][2]}")
            return index + 1  # Move past the closing parenthesis
        elif token_type == 'PLUS' or token_type == 'MINUS':
            parsing_steps.append(("Applying operator", f"{value}"))
            index = parse_expression(index + 1)  # Parse the next expression
            return index
        else:
            raise SyntaxError(f"Unexpected token {token_type} at line {line_number}")

    index = 0
    while index < len(tokens):
        token_type, value, line_number = tokens[index]
        if token_type == 'INT' or token_type == 'FLOAT' or token_type == 'CHAR':
            # Declaration statement
            if tokens[index + 1][0] != 'ID':
                raise SyntaxError(f"Expected ID at line {tokens[index + 1][2]}")
            if tokens[index + 2][0] != 'ASSIGN':
                raise SyntaxError(f"Expected ASSIGN at line {tokens[index + 2][2]}")
            index = parse_expression(index + 3)  # Parse the expression after '='
            if tokens[index][0] != 'SEMICOLON':
                raise SyntaxError(f"Expected SEMICOLON at line {tokens[index][2]}")
            index += 1  # Move past the semicolon
        else:
            raise SyntaxError(f"Unexpected token {token_type} at line {line_number}")

    # Return the parsing steps and results
    return parsing_steps


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
