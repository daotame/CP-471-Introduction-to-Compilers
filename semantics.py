from lex import tokens


def Semantics_LogError(logerror, filename):
    print("Writing to Error File...")

    with open(filename, "a") as file: 
        file.write(logerror + "\n") 
    
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
            if token[1] in ['def', 'while', 'if', 'else', 'int', 'double']:
                current_scope = token[1]
                print(current_scope)
            # Add keyword to symbol table
            symbol_table.append([i+1, token[1], 'Keyword', current_scope])
        elif token[0] == 'id':
            # Check if identifier is a variable or function
            if i < len(tokens) - 2  and tokens[i+1][1] == '(':
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
                
            elif token[1] == '=':
                # Check if types match for assignment
                if symbol_table[i-1][3] != symbol_table[i+1][3]:
                    logerror = (f"Type mismatch error at line {token[0]}: {symbol_table[i-1][1]} of type {symbol_table[i-1][3]} cannot be assigned to {symbol_table[i+1][1]} of type {symbol_table[i+1][3]}")
                    print(logerror)
                    Semantics_LogError(logerror, file_name_4)

            elif token[0] in ['comp', 'bool']:  # Comparison operators and boolean operators
                # Check if types match for comparison
                if symbol_table[i-1][3] != symbol_table[i+1][3]:
                    logerror = (f"Type mismatch error at line {token[0]}: {symbol_table[i-1][1]} of type {symbol_table[i-1][3]} cannot be compared to {symbol_table[i+1][1]} of type {symbol_table[i+1][3]}")
                    print(logerror)
                    Semantics_LogError(logerror, file_name_4)


            elif token[1] == 'return':
                # Get the expected return type of the function
                expected_return_type = symbol_table[current_scope][3][0]

                # Get the actual return type
                actual_return_type = symbol_table[i+1][3]

                # Check if the types match
                if expected_return_type != actual_return_type:
                    logerror = (f"Return type mismatch error at line {token[0]}: Expected {expected_return_type}, but got {actual_return_type}")
                    print(logerror)
                    Semantics_LogError(logerror, file_name_4)

            elif token[1] in ['od', 'fed', 'fi']:
                # Remove the symbol table for the current scope
                symbol_table = symbol_table[:current_scope]

                # Move back up to the parent scope
                current_scope = symbol_table[-1][3][1]

            else:
                variable_name = token[1]
                variable_type = current_scope  # Initialize variable type with current scope
                #print(variable_type)
                for entry in reversed(symbol_table):
                    if entry[1] == variable_name and entry[2] == 'Variable':
                        #print(entry[1])
                        #print(entry[2])
                        if entry[3] != variable_type:
                            #print(entry[3])
                            logerror = (f"Type mismatch error at line {i+1} {token[0]}: {variable_name} was previously declared with type {entry[3]}, cannot declare again with type {variable_type}")
                            print(logerror)
                            Semantics_LogError(logerror, file_name_4)
                        break
                    elif entry[2] == 'Keyword':
                        variable_type = entry[3]  # Update variable type with scope from last scope-defining keyword

                symbol_table.append([i+1, variable_name, 'Variable', current_scope])
              
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

