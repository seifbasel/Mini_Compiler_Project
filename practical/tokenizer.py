import re

# <program>        ::= <declaration>*
# <declaration>    ::= <type> <ID> "=" <value> ";"
# <type>           ::= "int"
# <value>          ::= <NUMBER>

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

# test code
code = '''
int a = 5;
int b = 3;
'''

# Get the tokens
tokens_list = list(lexer(code))

# Print the tokens
print("Tokens:")
for token in tokens_list:
    print(token)
