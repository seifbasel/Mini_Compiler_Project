import re

# Define tokens
tokens = [
    ('NUMBER', r'\d+(\.\d+)?'),  # Pattern for integers and floats
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'\/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('ASSIGN', r'\='),
    ('INT', r'int'),
    ('FLOAT', r'float'),
    ('CHAR', r'char'),
    ('CHAR_LITERAL', r'\'[^\']*\''),  # Pattern for character literals
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SEMICOLON', r'\;'),
    ('NEWLINE', r'[^\S\r\n]*\n'),  # Match entire line until newline character
    ('WHITESPACE', r'\s+'),
]

# Lexer function
def lexer(code):
    pos = 0
    line_number = 1
    declared_identifiers = set()  # Keep track of declared identifiers
    current_scope = None  # Current scope
    while pos < len(code):
        matched = False
        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':
                    if token_type == 'NEWLINE':
                        line_number += 1
                    elif token_type == 'ID':
                        identifier = value
                        if identifier in declared_identifiers and current_scope == identifier:
                            raise Exception(f"Identifier '{identifier}' already defined")
                        declared_identifiers.add(identifier)
                        yield (token_type, value, line_number)
                    elif token_type == 'LPAREN':
                        current_scope = None  # Start of a new scope
                    elif token_type == 'RPAREN':
                        current_scope = None  # End of the current scope
                    else:
                        yield (token_type, value, None)  # No line number for other tokens
                pos = match.end()
                matched = True
                break
        if not matched:
            raise Exception('Unexpected character: ' + code[pos])

# Define classes for grammar rules
class Program:
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def __str__(self):
        return str(self.statement_list)

class StatementList:
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return '\n'.join(str(statement) for statement in self.statements)

class Statement:
    def __init__(self, statement_type):
        self.statement_type = statement_type

    def __str__(self):
        return str(self.statement_type)

class Declaration:
    def __init__(self, data_type, identifier, expression):
        self.data_type = data_type
        self.identifier = identifier
        self.expression = expression

    def __str__(self):
        return f"{self.data_type} {self.identifier} = {self.expression}"

class Assignment:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __str__(self):
        return f"{self.identifier} = {self.expression}"

class Type:
    def __init__(self, data_type):
        self.data_type = data_type

    def __str__(self):
        return self.data_type

class Expression:
    def __init__(self, term, op=None, expression=None):
        self.term = term
        self.op = op
        self.expression = expression

    def __str__(self):
        if self.op:
            return f"{self.expression} {self.op} {self.term}"
        else:
            return str(self.term)

class Term:
    def __init__(self, factor, op=None, term=None):
        self.factor = factor
        self.op = op
        self.term = term

    def __str__(self):
        if self.op:
            return f"{self.term} {self.op} {self.factor}"
        else:
            return str(self.factor)

class Factor:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

def parse_statement(tokens):
    token_type, value, line_number = next(tokens)
    if token_type == 'INT' or token_type == 'FLOAT' or token_type == 'CHAR':
        data_type = Type(value)
        token_type, value, line_number = next(tokens)
        if token_type == 'ID':
            identifier = value
            token_type, value, line_number = next(tokens)
            if token_type == 'ASSIGN':
                expression = parse_expression(tokens)
                token_type, value, line_number = next(tokens)
                if token_type == 'SEMICOLON':
                    return Declaration(data_type, identifier, expression)
                else:
                    raise Exception(f"Expected SEMICOLON after {expression}")
            else:
                raise Exception(f"Expected ASSIGN token after {identifier}")
        else:
            raise Exception(f"Expected ID token after {data_type}")
    elif token_type == 'ID':
        identifier = value
        token_type, value, line_number = next(tokens)
        if token_type == 'ASSIGN':
            expression = parse_expression(tokens)
            token_type, value, line_number = next(tokens)
            if token_type == 'SEMICOLON':
                return Assignment(identifier, expression)
            else:
                raise Exception(f"Expected SEMICOLON after {expression}")
        else:
            raise Exception(f"Expected ASSIGN token after {identifier}")
    else:
        raise Exception(f"Unexpected token: {token_type}")


def parse_expression(tokens):
    term = parse_term(tokens)
    try:
        token_type, value, line_number = next(tokens)
        if token_type in ['PLUS', 'MINUS']:
            op = value
            expression = parse_expression(tokens)
            return Expression(term, op, expression)
        else:
            return term
    except StopIteration:
        return term

def parse_term(tokens):
    factor = parse_factor(tokens)
    try:
        token_type, value, line_number = next(tokens)
        if token_type in ['TIMES', 'DIVIDE']:
            op = value
            term = parse_term(tokens)
            return Term(factor, op, term)
        else:
            return factor
    except StopIteration:
        return factor

def parse_factor(tokens):
    token_type, value, line_number = next(tokens)
    if token_type == 'NUMBER' or token_type == 'CHAR_LITERAL' or token_type == 'ID':
        return Factor(value)
    elif token_type == 'LPAREN':
        expression = parse_expression(tokens)
        token_type, value, line_number = next(tokens)
        if token_type == 'RPAREN':
            return expression
        else:
            raise Exception(f"Expected RPAREN token after expression")
    else:
        raise Exception(f"Unexpected token: {token_type}")

def parse(tokens):
    statements = []
    while True:
        try:
            statement = parse_statement(tokens)
            statements.append(statement)
        except StopIteration:
            break
    return Program(StatementList(statements))

# Example usage
code = '''int x =5;
float y=3.14;
char c ='A';
float z =x + y;
'''

token_generator = lexer(code)
parsed_program = parse(token_generator)
print(parsed_program)
