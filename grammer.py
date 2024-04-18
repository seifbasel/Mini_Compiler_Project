
# grammer

# <program> ::= <statement>*

# <statement> ::= <expression> | <if_statement> | <while_statement>

# <if_statement> ::= 'if' '(' <expression> ')' '{' <statement>* '}' <else_if_statement> <else_statement>?

# <else_if_statement> ::= 'else if' '(' <expression> ')' '{' <statement>* '}' <else_if_statement>?

# <else_statement> ::= 'else' '{' <statement>* '}'

# <while_statement> ::= 'while' '(' <expression> ')' '{' <statement>* '}'


# <expression> ::= <term> | <expression> '+' <term> | <expression> '-' <term>
# <term> ::= <factor> | <term> '*' <factor> | <term> '/' <factor>
# <factor> ::= <integer> | '(' <expression> ')' | <comparison>

# <comparison> ::= <expression> ('==' | '!=' | '<' | '<=' | '>' | '>=' | '&&' | '||') <expression>

# <integer> ::= ('0' | <non_zero_digit> <digit>*)
# <non_zero_digit> ::= ('1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9')
# <digit> ::= <non_zero_digit> | '0'
