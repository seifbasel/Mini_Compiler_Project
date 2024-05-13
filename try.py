import re

def lexer(code):
    tokens = [
        ('number', r'\d+'),
        ('assign', r'='),
        ('int', r'int'),
        ('id', r'[a-z]'),
        ('semicolon', r';'),
    ]
    for token_type, pattern in tokens:
        for match in re.finditer(pattern, code):
            yield (token_type, match.group())

def symbol_table(code):
    table = {}
    data_type = None
    identifier = None
    for token_type, value in lexer(code):
        if token_type == 'int':
            data_type = value
        elif token_type == 'id':
            identifier = value
            table[identifier] = {'type': data_type, 'value': None}
        elif token_type == 'assign':
            pass  # No need to do anything here
        elif token_type == 'number' and identifier is not None:
            table[identifier]['value'] = value
    return table

code = '''
int a = 5;
int b = 3;
'''
print("Symbol Table:")
for identifier, details in symbol_table(code).items():
    print(f"Identifier: {identifier}, Type: {details['type']}, Value: {details['value']}")
