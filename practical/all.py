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
    parse_tree = []
    token_list = list(tokens)
    i = 0
    while i < len(token_list):
        if token_list[i][0] == 'int':
            if token_list[i+1][0] == 'id' and token_list[i+2][0] == 'assign' and token_list[i+3][0] == 'number' and token_list[i+4][0] == 'semicolon':
                data_type = token_list[i][1]
                identifier = token_list[i+1][1]
                value = token_list[i+3][1]
                symbol_table[identifier] = {'type': data_type, 'value': value}
                
                # Construct the parse tree for this statement
                statement = {
                    'type': 'declaration',
                    'data_type': data_type,
                    'identifier': identifier,
                    'value': value
                }
                parse_tree.append(statement)
                
                i += 5
            else:
                raise SyntaxError("Invalid syntax for declaration")
        else:
            raise SyntaxError("Expected type declaration")
    
    return symbol_table, parse_tree

def print_tree(parse_tree):
    for statement in parse_tree:
        print(f"  {statement['identifier']}")
        print(f"   |")
        print(f"  {statement['data_type']} = {statement['value']}")


code = '''
int a = 1;
int b = 2;
int c = 3;
'''

tokens_list=lexer(code)
print('token_tybe | token')
for i,x in tokens_list:
    
    print(i,x)
    
    
tokens_gen = lexer(code)
symbol_table, parse_tree = parse(tokens_gen)

print("Symbol Table:")
for identifier, details in symbol_table.items():
    print(f"Identifier: {identifier}, Type: {details['type']}, Value: {details['value']}") 

print("\nParse Tree:")
print_tree(parse_tree) 