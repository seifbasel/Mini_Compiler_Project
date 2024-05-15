import re
tokens=[
    ('int',r'int'),
    ('id',r'[a-z]'),
    ('assign',r'\='),
    ('number',r'\d+'),
    ('semicolon',r'\;'),
    ('newline',r'\n'),
    ('space',r'\s'),
]
code=""" 
int a=1;
int b=2;
"""
def lexer(code):
    pos=0
    while pos<len(code):
        for token_tybe,pattern in tokens:
            match=re.match(pattern,code[pos:])
            if match:
                value=match.group(0)
                if token_tybe!="newline" and token_tybe!="space":
                    yield(token_tybe,value)
                pos+=match.end()
                break
            
            
tokens_list=lexer(code)
for i,x in tokens_list:
    print(i,x)