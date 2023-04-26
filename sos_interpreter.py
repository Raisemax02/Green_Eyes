import os
import subprocess

# Definition of the instructions class
class instructions:
    # Method for printing the value of a variable
    def print_var(self, tokens):
        if len(tokens) != 1:
            raise ValueError("Syntax error: expected a single variable")
        var_name = tokens[0]
        if var_name in variables:
            var_value = variables[var_name]  # get the value from the variable
            print(var_value)
        else:
            raise ValueError(f"Variable '{var_name}' is not defined")

    # Method for creating a new variable
    def create_var(self, tokens):
        var_name = tokens[0]
        if tokens[1] != '=':
            raise ValueError("Syntax error: expected '='")
        var_value = " ".join(tokens[2:])
        variables[var_name] = var_value

    # Method for executing a system command
    def execute_command(self, tokens):
        if len(tokens) == 0:
            raise ValueError("Syntax error: expected a command")
        command = " ".join(tokens)
        try:
            result = subprocess.check_output(command, shell=True, universal_newlines=True)
            print(result)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def exit_program(self, tokens):
        if len(tokens) > 0:
            raise ValueError("Syntax error: 'quit' does not accept arguments")
        print("Exiting program.")
        print("It was a pleasure working with you and always remember to say SOS")
        exit()

# Function to start the program
def start_program():
    choice = input("Do you want to run a .sos program? (y/n) ")
    if choice.lower() == "y":
        file_name = input("Enter the name of the .sos file: ")
        if not file_name.endswith(".sos"):
            print("Error: file must have .sos extension")
            return
        if not os.path.exists(file_name):
            print(f"Error: file '{file_name}' does not exist")
            return
        instructions = read_sos_file(file_name)
        for instr in instructions:
            keyword = instr[0]
            if keyword in sos_keywords:
                sos_keywords[keyword](instr[1:])
            else:
                print(f"Error: unrecognized keyword '{keyword}'")
    elif choice.lower() == "n":
        while True:
            line = input("> ")
            tokens = tokenize(line)
            keyword = tokens[0]
            if keyword in sos_keywords:
                sos_keywords[keyword](tokens[1:])
            else:
                print(f"Error: unrecognized keyword '{keyword}'")
    else:
        print(f"Error: invalid choice '{choice}'")

# Function to split a line into words
def tokenize(line):
    # Remove the end-of-line character
    line = line.strip()
    # Split the line into words
    tokens = line.split()
    return tokens

def read_sos_file(file_name):
    if not file_name.endswith(".sos"):
        print("Error: incorrect file extension. File must have .sos extension")
        return []

    with open(file_name, "r") as f:
        lines = f.readlines()

    instructions = []
    for line in lines:
        # Remove the end-of-line character
        line = line.strip()

        # Ignore empty lines or comments
        if not line or line.startswith("#"):
            continue

        # Split the line into words
        tokens = line.split()

        #  Add instructions to the list
        instructions.append(tokens)


    return instructions

# Dictionary that maps sos keywords to functions
sos_keywords = {
    "sos":  instructions().print_var,   #sos(var_name)
    "Sos":  instructions().create_var,  #Sos(var_name, var_value)
    "soo":  instructions().execute_command, #soo(command)
    "quit": instructions().exit_program #quit()
}

# Program start
if __name__ == "__main__":
    variables = {}
    start_program()
