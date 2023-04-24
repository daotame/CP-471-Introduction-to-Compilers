from lex import tokens
import os, sys

#Pre-Processing
grammar = {
    "<program>": ["<fdecls>", "<declarations>", "<statement_seq>"],
    "<fdecls>": ["<fdec>", "<fdecls'>"],
    "<fdecls'>": [";", "<fdecls>", "ε"],
    "<fdec>": ["def", "<type>", "<fname>", "(", "<params>", ")", "<declarations>", "<statement_seq>", "fed"],
    "<params>": ["<type>", "<var>", "<params'>"],
    "<params'>": [",", "<params>", "ε"],
    "<fname>": ["<id>"],
    "<declarations>": ["<decl>", "<declarations'>"],
    "<declarations'>": [";", "<declarations>", "ε"],
    "<decl>": ["<type>", "<varlist>"],
    "<type>": ["int", "double"],
    "<varlist>": ["<var>", "<varlist'>"],
    "<varlist'>": [",", "<varlist>", "ε"],
    "<statement_seq>": ["<statement>", "<statement_seq'>"],
    "<statement_seq'>": [";", "<statement_seq>", "ε"],
    "<statement>": ["<var>", "=", "<expr>", "<if_statement>", "<while_statement>", "print", "<expr>", "return", "<expr>"],
    "<if_statement>": ["if", "<bexpr>", "then", "<statement_seq>", "<if_statement'>"],
    "<if_statement'>": ["else", "<statement_seq>", "fi"],
    "<while_statement>": ["while", "<bexpr>", "do", "<statement_seq>", "od"],
    "<expr>": ["<term>", "<expr'>"],
    "<expr'>": ["+", "<term>", "<expr'>", "-", "<term>", "<expr'>", "ε"],
    "<term>": ["<factor>", "<term'>"],
    "<term'>": ["*", "<factor>", "<term'>", "/", "<factor>", "<term'>", "%", "<factor>", "<term'>", "ε"],
    "<factor>": ["<var>", "<number>", "(", "<expr>", ")", "<fname>", "(", "<exprseq>", ")"],
    "<exprseq>": ["<expr>", "<exprseq'>"],
    "<exprseq'>": [",", "<exprseq>", "ε"],
    "<bexpr>": ["<bterm>", "<bexpr'>"],
    "<bexpr'>": ["or", "<bterm>", "<bexpr'>", "ε"],
    "<bterm>": ["<bfactor>", "<bterm'>"],
    "<bterm'>": ["and", "<bfactor>", "<bterm'>", "ε"],
    "<bfactor>": ["(", "<bexpr>", ")", "not", "<bfactor>", "<expr>", "<comp>", "<expr>"],
    "<comp>": ["<", ">", "==", "<=", ">=", "<>"],
    "<var>": ["<id>", "<var'>"],
    "<var'>": ["[", "<expr>", "]", "ε"],
    "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
    "<digit>": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    "<id>": ["<letter>", "<id'>"],
    "<id'>": ["<letter>", "<id'>", "<digit>", "<id'>", "ε"],
    "<number>": ["<integer>", "<double>"],
    "<integer>" : ["<digit>", "<integer'>"],
    "<integer'>" : ["<digit>", "<integer'>", "ε"],
    "<double>" : ["<integer>", "<integer>", "<integer>" ]
}

FIRST = {
    "<program>": {"int", "double", "<id>", "if", "while", "print", "return"},
    "<fdecls>": {"def"},
    "<fdecls'>": {";", "ε"},
    "<fdec>": {"def"},
    "<params>": {"int", "double", "<id>"},
    "<params'>": {",", "ε"},
    "<fname>": {"<id>"},
    "<declarations>": {"int", "double", "ε"},
    "<declarations'>": {";", "ε"},
    "<decl>": {"int", "double"},
    "<type>": {"int", "double"},
    "<varlist>": {"<id>"},
    "<varlist'>": {",", "ε"},
    "<statement_seq>": {"<id>", "if", "while", "print", "return"},
    "<statement_seq'>": {";", "ε"},
    "<statement>": {"<id>", "if", "while", "print", "return"},
    "<if_statement>": {"if"},
    "<if_statement'>": {"else", "fi"},
    "<while_statement>": {"while"},
    "<expr>": {"<id>", "<number>", "(", "<fname>", "<term>"},
    "<expr'>": {"+", "-", "ε"},
    "<term>": {"<id>", "<number>", "(", "<fname>"},
    "<term'>": {"*", "/", "%", "ε"},
    "<factor>": {"<id>", "<number>", "(", "<fname>"},
    "<exprseq>": {"<id>", "<number>", "(", "<fname>", "ε"},
    "<exprseq'>": {",", "ε"},
    "<bexpr>": {"<id>", "<number>", "(", "<fname>", "(", "not", "("},
    "<bexpr'>": {"or", "ε"},
    "<bterm>": {"<id>", "<number>", "(", "<fname>", "(", "not", "("},
    "<bterm'>": {"and", "ε"},
    "<bfactor>": {"(", "not", "<id>", "<number>", "(", "<fname>", "<expr>"},
    "<comp>": {"<", ">", "==", "<=", ">=", "<>"},
    "<var>": {"<id>"},
    "<var'>": {"[", "ε"},
    "<letter>": {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"},
    "<digit>": {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"},
    "<id>": {"<letter>"},
    "<id'>": {"<letter>", "<digit>", "ε"},
    "<number>": {"<integer>", "<double>"},
    "<integer>": {"<digit>"},
    "<integer'>": {"<digit>", "ε"},
    "<double>": {"<integer>"}
}

FOLLOW = {
    "<program>": {"$"},
    "<fdecls>": {"def", "int", "double", "$"},
    "<fdecls'>": {";", "$"},
    "<fdec>": {"def", "$"},
    "<params>": {"int", "double", "$"},
    "<params'>": {",", ")"},
    "<fname>": {"<id>"},
    "<declarations>": {"<type>", "$"},
    "<declarations'>": {";", "$"},
    "<decl>": {"int", "double", "$"},
    "<type>": {"int", "double", "$"},
    "<varlist>": {"<id>", "$"},
    "<varlist'>": {",", "]"},
    "<statement_seq>": {"<var>", "if", "while", "print", "return", "$"},
    "<statement_seq'>": {";", "$"},
    "<statement>": {"<var>", "<if_statement>", "<while_statement>", "print", "return", "$"},
    "<if_statement>": {"if", "$"},
    "<if_statement'>": {"else", "fi", "$"},
    "<while_statement>": {"while", "$"},
    "<expr>": {"<var>", "<number>", "(", "<fname>", "$"},
    "<expr'>": {"+", "-", "$"},
    "<term>": {"<var>", "<number>", "(", "<fname>", "$"},
    "<term'>": {"*", "/", "%", "$"},
    "<factor>": {"<var>", "<number>", "(", "<fname>", "$"},
    "<exprseq>": {"<expr>", "$"},
    "<exprseq'>": {",", "$"},
    "<bexpr>": {"(", "not", "<var>", "<number>", "(", "$"},
    "<bexpr'>": {"or", "$"},
    "<bterm>": {"(", "not", "<var>", "<number>", "(", "$"},
    "<bterm'>": {"and", "$"},
    "<bfactor>": {"(", "not", "<var>", "<number>", "(", "<comp>", "$"},
    "<comp>": {"<", ">", "==", "<=", ">=", "<>", "$"},
    "<var>": {"<id>", "$"},
    "<var'>": {"[", "]"},
    "<letter>": {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "$"},
    "<digit>": {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "$"},
    "<id>": {"<letter>", "$"},
    "<id'>": {"<letter>", "<digit>", "$"},
    "<number>": {"<integer>", "<double>", "$"},
    "<integer>": {"<digit>", "$"},
    "<integer'>": {"<digit>", "$"},
    "<double>": {"<integer>", "$"}
}

print("\n")
print("Syntax Analysis")

#LL1 Parsing begins, finding non-terminals and terminals first

def create_terminals_nonterminals(grammar):
    terminals = []
    non_terminals = []

    for rule in grammar:
        non_terminals.append(rule)
        for symbol in grammar[rule]:
            if symbol not in non_terminals and symbol not in terminals:
                terminals.append(symbol)

    print("\n")
    print("Terminals: ", terminals)
    print("\n")
    print("Non-terminals: ", non_terminals)
    return terminals, non_terminals

def parse_table_create(productions, non_terminals, terminals):
    table = {}
    for nt in non_terminals:
        for t in terminals:
            table[(nt, t)] = None

    for nt, productions in productions.items():
        for prod in productions:
            first_set = set()
            for i, symbol in enumerate(prod.split()):
                symbol = str(symbol)
                if symbol in non_terminals:
                    # Check if `symbol` is in `first_sets`
                    if symbol not in FIRST:
                        #print("Symbol " + symbol + " not found in `first_sets` dictionary")
                        break
                    # Check if `first_sets[symbol]` is a set
                    if not isinstance(FIRST[symbol], set):
                        print(f"`first_sets[{symbol}]` is not a set")
                        break
                    first_set |= FIRST[symbol]
                    if 'ε' not in FIRST[symbol]:
                        break
                else:
                    first_set.add(symbol)
                    break
            else:
                first_set.add('ε')

            for terminal in first_set:
                if terminal != 'ε':
                    table[(nt, terminal)] = prod

            if 'ε' in first_set:
                for terminal in FOLLOW[nt]:
                    table[(nt, terminal)] = prod

    # Print the LL(1) parser table
    print('LL(1) Parser Table:')
    print('\t' + '\t'.join(terminals))
    for nt in non_terminals:
        row = [nt]
        for t in terminals:
            prod = table[(nt, t)]
            if prod is None:
                row.append('')
            else:
                row.append(f'{nt} -> {prod}')
        print('\t'.join(row))

    return table

def parse(tokens, parse_table):

    # Initialize the stack and pointer to the first token
    stack = ['$']
    pointer = 0

    # Loop until the stack is empty or a syntax error is found
    while stack:
        # Pop the top symbol from the stack
        symbol = stack.pop()

        # If the symbol is a non-terminal, check the parse table
        if symbol in non_terminals:
            # Get the current token
            if pointer >= len(tokens):
                # End of input, use '$'
                token = '$'
            else:
                token = tokens[pointer][1]

            # Look up the production rule in the parse table
            prod = parse_table.get((symbol, token))

            # If no production rule is found, syntax error
            if prod is None:
                print('Syntax error for Token' + token)
                Syntax_ErrorLog(tokens, file_name_3)
                return False

            # Push the symbols of the production rule onto the stack in reverse order
            for sym in reversed(prod.split()):
                if sym != 'ε':
                    stack.append(sym)

        # If the symbol is a terminal, check if it matches the current token
        elif symbol in terminals:
            # Check if the current token matches the symbol
            if pointer >= len(tokens) or tokens[pointer][0] != symbol:
                print('Syntax error for Token ' + token)
                Syntax_ErrorLog(tokens, file_name_3)
                return False

            # Move to the next token
            pointer += 1

        # If the symbol is the end-of-input marker, parsing is successful
        elif symbol == '$':
            print('Parsing successful')
            return True

    # If the stack is empty and we haven't found the end-of-input marker, syntax error
    print('Syntax error')
    return False


def Syntax_ErrorLog(word, filename):
    print("Writing to Error File...")

    with open(filename, "a") as file: 
        file.write("Error: invalid syntax for token " + word)
    
    print("\n")

file_name_3 = "SyntaxErrorLog.txt"
with open(file_name_3, "w") as file: #makes sure to clear the file manually before running it again
        file.write('')

terminals, non_terminals = create_terminals_nonterminals(grammar)
parse_table = parse_table_create(grammar, non_terminals, terminals)
print("\n")
print("\n")
parse(tokens, parse_table)
