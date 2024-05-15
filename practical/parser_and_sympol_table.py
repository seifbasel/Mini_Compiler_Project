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

def parse(tokens):
    symbol_table = {}
    token_list = list(tokens)
    i = 0
    while i < len(token_list):
        if token_list[i][0] == 'int':
            if token_list[i+1][0] == 'id' and token_list[i+2][0] == 'assign' and token_list[i+3][0] == 'number' and token_list[i+4][0] == 'semicolon':
                data_type = token_list[i][1]
                identifier = token_list[i+1][1]
                value = token_list[i+3][1]
                symbol_table[identifier] = {'type': data_type, 'value': value}
                i += 5
            else:
                raise SyntaxError("Invalid syntax for declaration")
        else:
            raise SyntaxError("Expected type declaration")
    
    return symbol_table

code = '''
int a = 1;
int b = 2;
int c = 3;
'''

tokens_gen = lexer(code)
symbol_table = parse(tokens_gen)

print("Symbol Table:")
for identifier, details in symbol_table.items():
    print(f"Identifier: {identifier}, Type: {details['type']}, Value: {details['value']}")