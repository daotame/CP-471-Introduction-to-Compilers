import re
from lex import file_name


print("\n")
print("Code Generation:")

with open(file_name, "r") as f:
    file_contents = f.read()

#print(file_contents)
#lines = file_contents.split("\n")
#print(lines)
#for line in lines:
#    print(line)
tac = []
label_count = 0
temp_count = 0


# Regular expressions for parsing the code
declaration_pattern = re.compile(r"def\s+int\s+(\w+)\(([^)]*)\)\s*{([^}]+)}")
assignment_pattern = re.compile(r"(\w+)\s*=\s*(.+)")
binary_pattern = re.compile(r"(.+)\s*([+\-*/])\s*(.+)")
call_pattern = re.compile(r"print\s+(\w+)\(([^)]*)\)")
while_pattern = re.compile(r"while\((.+)\)\s*do")
print_pattern = re.compile(r"print\((\w+)\)")
if_pattern = re.compile(r"if\s*\((.+?)\)\s*then\s*([^}]+?)(?:else\s*([^}]+?))?\s*fi")
return_pattern = re.compile(r"return\s*\((.+)\)")
label_pattern = re.compile(r"L(\d+)")


tac = []
label_count = 0
temp_count = 0


# Parse function declarations
if "def" in file_contents:
    function_name = file_contents.split("(")[0].split()[-1]
    function_params = file_contents.split("(")[1].split(")")[0].split(",")
    #print(function_name)
    #print(function_params)
    tac.append(f"function {function_name}{function_params}")
    statements = [s.strip() for s in file_contents.split(";") if s.strip()]
    for s in statements:
        # If statements
        im = if_pattern.search(s)
        if im:
            label_count += 1
            condition = im.group(1)
            then_label = f"L{label_count}"
            tac.append(f"if {condition} goto {then_label}")
            else_label = f"L{label_count+1}"
            tac.append(f"goto {else_label}")
            tac.append(f"{then_label}:")
            # Parse the then block
            for sub_s in s[im.end():].split(";"):
                sub_s = sub_s.strip()
                # Check for return statements
                rm = return_pattern.search(sub_s)
                if rm:
                    value = rm.group(1)
                    tac.append(f"return {value}")
            tac.append(f"goto L{label_count+2}")
            tac.append(f"{else_label}:")
            # Parse the else block
            for sub_s in s[im.end():].split(";"):
                sub_s = sub_s.strip()
                # Check for return statements
                rm = return_pattern.match(sub_s)
                if rm:
                    value = rm.group(1)
                    tac.append(f"return {value}")
            tac.append(f"L{label_count+2}:")
            continue


# Parse declarations
declarations = declaration_pattern.findall(file_contents)
for d in declarations:
    for var in d:
        tac.append(f"declare {var}")

def parse_statements():
    # Parse statements
    temp_count = 0
    label_count = 0
    statements = [s.strip() for s in file_contents.split(";") if s.strip()]
    for s in statements:
        # Assignments
        m = assignment_pattern.match(s)
        if m:
            dest, expr = m.groups()
            # Check if the expression is binary
            bm = binary_pattern.match(expr)
            if bm:
                op1, op, op2 = bm.groups()
                temp = f"t{temp_count}"
                tac.append(f"{op1} = {temp}")
                tac.append(f"{temp} = {op2} {op} {dest}")
                temp_count += 1
            else:
                tac.append(f"{dest} = {expr}")
        # While loops
        m = while_pattern.match(s)
        if m:
            label_count += 1
            start_label = f"L{label_count}"
            end_label = f"L{label_count+1}"
            condition = m.group(1)
            tac.append(f"{start_label}:")
            # Check if the condition is binary
            bm = binary_pattern.match(condition)
            if bm:
                op1, op, op2 = bm.groups()
                tac.append(f"if {op1} {op} {op2} goto {end_label}")
            else:
                tac.append(f"if not {condition} goto {end_label}")
            # Loop body
            for sub_s in s[m.end():].split(";"):
                sub_s = sub_s.strip()
                m = assignment_pattern.match(sub_s)
                if m:
                    dest, expr = m.groups()
                    # Check if the expression is binary
                    bm = binary_pattern.match(expr)
                    if bm:
                        op1, op, op2 = bm.groups()
                        temp = f"t{temp_count}"
                        tac.append(f"{op1} = {temp}")
                        tac.append(f"{temp} = {op2} {op} {dest}")
                        temp_count += 1
                    else:
                        tac.append(f"{dest} = {expr}")
            tac.append(f"goto {start_label}")
            tac.append(f"{end_label}:")
        # Print statements
        m = print_pattern.match(s)
        if m:
            tac.append(f"print {m.group(1)}")


parse_statements()
# Parse function call
call = call_pattern.search(file_contents)
if call:
    name = call.group(1)
    args = [a.strip() for a in call.group(2).split(",") if a.strip()]
    tac.append(f"param {args[0]}")
    tac.append(f"param {args[1]}")
    tac.append(f"call {name}, 2")
    temp_count += 1
    temp_var = f"t{temp_count}"
    tac.append(f"{temp_var} = return")
    tac.append(f"print {temp_var}")

# Print TAC
for i, t in enumerate(tac):
    print(f"{i+1}: {t}")
