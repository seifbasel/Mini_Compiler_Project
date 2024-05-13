import re

tokens = [
    ('number', r'\d+'),   
    ('assign', r'\='),
    ('int', r'int'),
    ('id', r'[a-z]'),  
    ('semicolon', r'\;'),
    ('newline', r'\n'),
    ('space', r'\s'),
]

def lexer(code):
    pos = 0
    while pos < len(code):
        for token_type, pattern in tokens:
            match = re.match(pattern, code[pos:])
            if match:
                value = match.group(0)
                if token_type != 'newline' and token_type != 'space':
                    yield (token_type, value)  
                pos += match.end()
                break 


def unordered_symbol_table(code):
    symbol_table = {}
    for token_type, value in lexer(code):
        if token_type == 'int':
            data_type = value   
        elif token_type == 'id':
            identifier = value
            if identifier not in symbol_table:
                symbol_table[identifier] = {
                    'type': data_type,
                    'value': None,
                }
        elif token_type == 'number' :
            symbol_table[identifier]['value'] = value

    return symbol_table

# Example usage
code = '''
int a = 1;
int b = 2;
int c= 3;
'''

# Get symbol table
symbol_table_unordered = unordered_symbol_table(code)

# Print the symbol table
print("Symbol Table:")
for identifier, details in symbol_table_unordered.items():
    print(f"Identifier: {identifier}, Type: {details['type']}, Value: {details['value']}")


