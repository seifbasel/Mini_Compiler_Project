import re
tokens=[
    ('number',r'\d+'),
    ('int',r'int'),
    ('id',r'[a-z]'),
    ('assign',r'\='),
    ('semicolon',r'\;'),
    ('newline',r'\n'),
    ('space',r'\s'),
    ]


def lexer(code):
    pos=0
    while pos<len(code):
        for  tokentybe,pattern in tokens:
            match=re.match(pattern,code[pos:])
            if match:
                value=match.group()
                if tokentybe !='newline' and tokentybe !='space':
                    yield(value,tokentybe)
                pos+=match.end()
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
