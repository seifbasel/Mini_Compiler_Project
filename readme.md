# Mini Compiler

This is a mini compiler implemented in Python that performs lexical analysis, parsing, and symbol table generation for a simple programming language. It demonstrates the concepts of tokenization, recursive descent parsing, and symbol table construction.

## Features

- **Lexical Analysis**: Tokenizes input code into tokens such as numbers, identifiers, keywords, and special symbols.
- **Parsing**: Implements a recursive descent parser to parse the input code based on a defined grammar.
- **Symbol Table Generation**: Constructs a symbol table that records information about variables such as their type, value, declaration line, and object address.

<!-- ## Grammer

<program>       ::= <declaration>*
<declaration>   ::= <type> <ID> "=" <value> ";"
<type>          ::= "int" | "float" | "char"
<value>         ::= <NUMBER> | <CHAR_LITERAL> -->


## Installation

To use this mini compiler, make sure you have Python 3.x installed on your system. Additionally, install the required dependencies by running:

```bash
pip install -r requirements.txt
