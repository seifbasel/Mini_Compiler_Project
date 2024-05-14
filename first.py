# Example grammar
grammar = {
    'E': [['T', 'E`']],
    'E`': [['+','T', 'E`'], ['ε']],
    'T': [['F', 'T`']],
    'T`': [['*','F', 'T`'],['ε']],
    'F': [['(','E',')'],['id']]
    }


'''first'''

def compute_first(grammar):
    first = {}
    
    for non_terminal in grammar.keys():
        first[non_terminal] = set()
    
    def compute_first_for_symbol(symbol):
       
        for production in grammar[symbol]:
            # Rule 1 : If the production is epsilon, add epsilon to the first set
            if 'ε' in production:
                first[symbol].add('ε')
            
            else:
                first_of_first_symbol = production[0]
                #Rule 2: If the first symbol is a terminal, add it to the first set
                if first_of_first_symbol not in grammar:
                    first[symbol].add(first_of_first_symbol)
                # Rule 3 :If the first symbol is a non-terminal, recursively compute its first set
                else:
                    compute_first_for_symbol(first_of_first_symbol)
                    first[symbol] = first[symbol].union(first[first_of_first_symbol])
    
    # Compute first set for each non-terminal
    for non_terminal in grammar.keys():
        compute_first_for_symbol(non_terminal)
    
    return first


first_sets = compute_first(grammar)
print("First functions")
for symbol in grammar:
    print(f'First({symbol}): {first_sets[symbol]}')