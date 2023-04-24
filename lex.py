
import re, os, sys, csv

def check_file_extension(file_name):
    # Get the extension of the file
    file_extension = file_name.split(".")[-1]

    # Check if the extension is ".cp"
    if file_extension == "cp":
        return True
    else:
        return False

def read_source_program(file_name):
    # Open the file in read mode
    with open(os.path.join(sys.path[0], file_name), 'r') as file: 
        # Read the contents of the file into the first buffer
        buffer1 = file.read()

        # Set the position in the file back to the beginning
        file.seek(0)

        # Read the contents of the file into the second buffer
        buffer2 = file.read()

        # Compare the two buffers to ensure that they match
        if buffer1 == buffer2:
            return buffer1
        else:
            raise Exception("Error: Double buffering failed.")

#Function to create tokens list
def create_tokens(text):
	#Defining Tokens
    tokens = []
    keyword_regex = re.compile("^(def|fed|if|then|else|fi|while|do|od|print|return|not|int|double)$")
    id_regex = re.compile("^[A-Za-z]+[A-Za-z0-9]*$")
    number_regex = re.compile("^[0-9]+(\.[0-9]+)?$")
    symbol_regex = re.compile("^[\+\-\*\/\%\=\(\)\[\]\;\,\.]$")
    comp_regex = re.compile("^(<|>|==|<=|>=|<>)$")
    words = re.findall("[\w\.]+|[\S]", text)
    print("\n")
    print(words)
    
    #creates the tokens
    for word in words:
        if keyword_regex.match(word):
            tokens.append(("keyword", word))
        elif id_regex.match(word):
            tokens.append(("id", word))
        elif number_regex.match(word):
            tokens.append(("number", word))
        elif symbol_regex.match(word):
            tokens.append(("symbol", word))
        elif comp_regex.match(word):
            tokens.append(("comp", word))
        else:
            #Goes into Panic Mode writng the error into error log file
            panic_mode(word, file_name_2)

    return tokens

#Function to create DFA
def create_dfa(tokens):
    # Define the states of the DFA
    states = []
    state = 0
    states.append(state)
    
    # Define the transitions of the DFA
    transitions = {}

    # Define the start state
    start_state = 0
    
    # Define the accept states
    accept_state = 0
    
    for token in tokens:
        # Get the type and value of the current token
        type = token[0]
        value = token[1]
        
        # Check if there is already a transition for the current type
        if type in transitions:
            # If there is a transition, add the value to the existing transition
            transition = transitions[type]
            transition[value] = state
            transitions[type] = transition
        else:
            # If there is no transition, create a new one and add it to the transitions
            state = state + 1
            states.append(state)
            transition = {value: state}
            transitions[type] = transition
        
    accept_state = states[-1]
    
    return (states, transitions, start_state, accept_state)


#Function to create Transition Table
def create_transition_table(dfa):
    states, transitions, start_state, accept_states = dfa
    transition_table = {}
    for state in states:
        transition_table[state] = {}
        for token_type, next_states in transitions.items():
            for token, next_state in next_states.items():
                transition_table[state][token] = next_state
    return transition_table

def load_transition_table_csv(transition_table):
    headers = list(transition_table[0].keys())
    with open('output.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        # write each row (dictionary) to the csv file
        for row in transition_table.values():
            writer.writerow(row)

    print('CSV file created successfully.')

#Helper Function to find line number, trying to fix this
def find_line_number(filename, word):
    with open(filename, "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines, 1):
            if word in line:
                return i



#Function for Panic Mode 
def panic_mode(word, filename):
    print("Invalid Token Found, Initiating Panic Mode")

    print("\n")
    print(f"Invalid Token '{word}' on line {find_line_number(filename, word)}.") 
    print("\n")
    print("Writing to Error File...")

    with open(filename, "a") as file: 
        file.write(f"Invalid Token '{word}' on line {find_line_number(filename, word)}.\n") 
    
    print("\n")
    print("Panic Mode Finished, Resuming Program")


file_name = "Test1.cp"
#file_name = "Test2.cp"
#file_name = "Test3.cp"
#file_name = "Test4.cp"
#file_name = "Test5.cp"
#file_name = "Test6.cp"
#file_name = "Test7.cp"
#file_name = "Test8.cp"
#file_name = "Test9.cp"
is_cp_file = check_file_extension(file_name)

if is_cp_file:
    print("The file has a '.cp' extension.")
else:
    print("The file does not have a '.cp' extension.")
    sys.exit(0)

file_name_2 = "ErrorLog.txt"
with open(file_name_2, "w") as file: #makes sure to clear the file manually before running it again
        file.write('') 
source_program = read_source_program(file_name)
print(source_program)
text = source_program
tokens = create_tokens(text)
dfa = create_dfa(tokens)
transition_table = create_transition_table(dfa)

print("\n")
print("Tokens")

print(tokens)
print("\n")
print("DFA")
print(dfa)
print("\n")
print("States:", dfa[0])
print("Transitions:", dfa[1])
print("Start state:", dfa[2])
print("Accept states:", dfa[3])

print("\n")

print("Transition table:")
print(transition_table)
load_transition_table_csv(transition_table)
