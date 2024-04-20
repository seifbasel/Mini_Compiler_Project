class SimpleLangParser:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def parse(self):
        return self.statement()

    def statement(self):
        if self.text[self.pos:self.pos + 3] == 'int':
            return self.declaration()
        else:
            return self.expression()

    def declaration(self):
        # Expecting 'int'
        if self.text[self.pos:self.pos + 3] == 'int':
            self.pos += 3
        else:
            raise SyntaxError("Expected 'int'")

        # Skip whitespace
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        # Expecting variable name
        var_name = self.identifier()

        # Skip whitespace
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        # Expecting '='
        if self.text[self.pos] == '=':
            self.pos += 1
        else:
            raise SyntaxError("Expected '='")

        # Skip whitespace
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        # Expecting value
        value = self.integer()

        # Skip whitespace
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        # Expecting ';'
        if self.text[self.pos] == ';':
            self.pos += 1
        else:
            raise SyntaxError("Expected ';'")

        return (var_name, value)

    def expression(self):
        return self.addition()

    def addition(self):
        result = self.multiplication()

        while self.pos < len(self.text) and self.text[self.pos] in ('+', '-'):
            operator = self.text[self.pos]
            self.pos += 1
            right = self.multiplication()
            if operator == '+':
                result += right
            else:
                result -= right

        return result

    def multiplication(self):
        result = self.term()

        while self.pos < len(self.text) and self.text[self.pos] in ('*', '/'):
            operator = self.text[self.pos]
            self.pos += 1
            right = self.term()
            if operator == '*':
                result *= right
            else:
                result /= right

        return result

    def term(self):
        if self.text[self.pos].isdigit():
            return self.integer()
        elif self.text[self.pos] == '(':
            self.pos += 1  # consume '('
            result = self.expression()
            self.pos += 1  # consume ')'
            return result
        else:
            raise SyntaxError("Unexpected token: " + self.text[self.pos])

    def integer(self):
        result = 0
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            result = result * 10 + int(self.text[self.pos])
            self.pos += 1
        return result

    def identifier(self):
        result = ''
        while self.pos < len(self.text) and self.text[self.pos].isalnum():
            result += self.text[self.pos]
            self.pos += 1
        return result


# Example usage:
parser = SimpleLangParser("int x=5;")
result = parser.parse()
print("Result:", result)
