from lex import tokens, find_line_number


def Semantics_LogError(word, filename):
    print("Writing to Error File...")

    with open(filename, "a") as file: 
        file.write(f"Invalid Token '{word}' on line {find_line_number(filename, word)}.\n") 
    
    print("\n")

def AnalyseSemantics(tokens):
    # Initialize symbol table and scope variables
    symbol_table = []
    current_scope = None

    # Define literal types
    literal_types = set(['number', 'string'])

    #Iterate over tokens and generate symbol table
    for i in range(len(tokens)):
        token = tokens[i]
        #print(token)
        if token[0] == 'keyword':
            # If keyword is a scope-defining keyword, set the current scope
            if token[1] in ['def', 'while', 'if', 'else']:
                current_scope = token[1]
            # Add keyword to symbol table
            symbol_table.append([i+1, token[1], 'Keyword', current_scope])
        elif token[0] == 'id':
            # Check if identifier is a variable or function
            if i < len(tokens) - 2  and tokens[i+1][1] == '(':
                #lookup(token[1], current_scope, symbol_table)
                # Extract function name and parameter types
                function_name = token[1]
                param_types = []
                j = i+2  # Start at index of first parameter token
                while tokens[j][1] != ')':  # Loop until end of parameter list
                    # Extract parameter type
                    param_type = ''
                    while tokens[j][1] not in [',', ')']:  # Build parameter type string
                        param_type += tokens[j][1]
                        j += 1
                    param_types.append(param_type.strip())  # Add parameter type to list
                    if tokens[j][1] == ',':  # Move to next parameter token
                        j += 1
                # Extract return type from previous token
                k = i-1
                while tokens[k][1] in ['*', '&']:  # Skip any pointer or reference symbols
                    k -= 1
                return_type = tokens[k][1]
                # Add function to symbol table with return type and parameter types
                symbol_table.append([i+1, function_name, 'Function', (return_type, param_types)])
                
            if token[1] == '=':
                # Check if the variable exists in the current scope or any parent scopes
                variable_name = symbol_table[i-1][1]
                found = False
                for j in range(i-1, -1, -1):
                    if symbol_table[j][1] == variable_name:
                        found = True
                        break
                    elif symbol_table[j][2] in ['Function', 'Keyword']:
                        break
                if not found:
                    # Log an error and enter panic mode
                    print(f"Error at line {token[0]}: Undeclared variable '{variable_name}'")
                    Semantics_LogError(variable_name, file_name_4)
                    # Perform panic mode
                    while token[1] != ';':
                        i += 1
                        token = tokens[i]
                    continue
        
                # Check if types match for assignment
                if symbol_table[j][3] != symbol_table[i+1][3]:
                    print(f"Type mismatch error at line {token[0]}: {symbol_table[j][1]} of type {symbol_table[j][3]} cannot be assigned to {symbol_table[i+1][1]} of type {symbol_table[i+1][3]}")

            if token[1] == 'return':
                # Get the expected return type of the function
                expected_return_type = symbol_table[current_scope][3][0]

                # Get the actual return type
                actual_return_type = symbol_table[i+1][3]

                # Check if the types match
                if expected_return_type != actual_return_type:
                    print(f"Return type mismatch error at line {token[0]}: Expected {expected_return_type}, but got {actual_return_type}")

            if token[1] in ['od', 'fed', 'fi']:
                # Remove the symbol table for the current scope
                symbol_table = symbol_table[:current_scope]

                # Move back up to the parent scope
                current_scope = symbol_table[-1][3][1]

            else:
                # If identifier is a variable, add to symbol table with type and scope from last scope-defining keyword
                symbol_table.append([i+1, token[1], 'Variable', current_scope])
                
        elif token[0] in literal_types:
            # Add literal to symbol table with type
            symbol_table.append([i+1, token[1], 'Literal', token[0]])

    # Update symbol table with variable types
    for i in range(len(symbol_table)):
        if symbol_table[i][2] == 'Variable':
            for j in range(i+1, len(symbol_table)):
                if symbol_table[j][2] == 'Keyword':
                    # If keyword is a scope-defining keyword, update variable type and scope
                    symbol_table[i][3] = (symbol_table[i][3], 'None')
                    if symbol_table[j][1] in ['def', 'while', 'if', 'else']:
                        symbol_table[i][3] = (symbol_table[i][3][0], symbol_table[j][1])
                    break

        
    # Print symbol table
    print('Line\tLexeme\tToken\tType')
    for row in symbol_table:
        print(f'{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}')


file_name_4 = "SemanticsErrorLog.txt"
with open(file_name_4, "w") as file: #makes sure to clear the file manually before running it again
        file.write('')

print("\n")
print("Semantics Analysis")
print("\n")
AnalyseSemantics(tokens)
