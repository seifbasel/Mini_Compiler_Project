import re 

tokens = [
    ('number',r'\d+'),
    ('assign',r'\='),
    ('int',r'int'),
    ('id',r'[a-z]'),
    ('semicolon',r'\;'),
    ('newline',r'\n'),
    ('space',r'\s'),
]

def lexer(code):
    pos=0
    while pos< len(code):
        for token_Type,pattern in tokens:
            match=re.match(pattern,code[pos:])
            if match:
                value=match.group(0)
                if token_Type!='newline'and token_Type!='space':
                    yield(token_Type,value)
                pos+=match.end()
                break
    

def sympol_table():
    sympol_table={}
    for token,tybe in lexer(code):
    


code='''
int a=1;
int b=2;
'''

tokenz=list(lexer(code))
for token, tybe in tokenz:
    print(token, tybe)

