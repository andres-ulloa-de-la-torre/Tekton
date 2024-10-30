
def divide_formulae(formula):


    chunk1 = ""
    chunk2 = ""
    mid = False

    for _ in range(len(formula)):


        if formula[_] == "|":

            mid = True
            continue

        if mid:

            chunk1 += formula[_] 
        
        else:

            chunk2 += formula[_] 

    return chunk1, chunk2



def parse_formulae(string):

    stripped = ''
    coefficients = []
    accelerators = []
    operators = []


    for idx, char in enumerate(string):

        if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:

            last_char = string[idx - 1]

            if last_char == ')' and char.isdigit():

                accelerators.append(int(char))

            elif last_char == '(' and char.isdigit():

                coefficients.append(int(char))

            
        elif char.lower() in [ 'i', 'e' , 'f' , 's', 'n' , 't', ' ']:

            stripped += char
        
        elif char.lower() in ['~', 'oo', '->', '|']:

            operators.append(char)
            stripped += char
        
        elif char in ['(', ')']:

            stripped += char
            
        else:

            raise ValueError(f'Invalid character: {char}')
        
        last_char = char

    if coefficients == []: 

        if len(operators) == 1: 

            coefficients = [1,1]

        elif len(operators) == 2: 

            coefficients = [1,1,1]

    
    return stripped, coefficients, operators, accelerators

            
if __name__ == '__main__': 
    pass