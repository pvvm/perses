import subprocess
import random
from test.generate_random_test import generate_test

def randomize_sort(elements):
    keys = list(elements.keys())
    random.shuffle(keys)
    aux = dict()
    for k in keys:
        aux[k] = elements[k]

    #print(aux)
    return dict(sorted(aux.items(), key=lambda x:x[1][1]))

def product_calc(elements):
    product = 1
    for e in elements:
        product *= (1 - elements[e][1])**(1 - elements[e][0])
    return product

def max_gain(elements):
    last_gain = 0
    ex = 0
    for e in elements:
        if elements[e][1] > 0:
            ex += 1

        current_gain = ex * product_calc(elements)

        if last_gain > current_gain:
            break

        elements[e][0] = 0 # step 2
        last_gain = current_gain

    return dict(sorted(elements.items(), key=lambda x:x[1][2]))

# Is this used anywhere?
#def CheckCondition(elements):
#    for e in elements:
#        if e[1] != 0.0 or e[1] != 1.0:
#            return False
#    return True

# "elements" is the list of elements to be reduced.
# "result" is the test outcome if it satisfied the test or not with exclusion.
def AdjustProbs(elements, result):
    # result F == 0, T == 1
    # excluded elements[i][0] == 0, in the subsequence == 1
    if result:
        for i in elements:
            if elements[i][0] == 0:
                elements[i][1] = 0
    else:
        product = 1.0
        for j in elements:
            product *= (1.0 - elements[j][1]) ** (1 - elements[j][0])
        for i in elements:
            if elements[i][0] == 0 and elements[i][1] != 0.0:
                elements[i][1] /= (1 - product)
        

#def probDD(sequence, test_function):
    # probabilities of each element in the optimal solution
#    probabilities = sequence.copy()
    # current optimal solution
#    next_test_sequence = sequence.copy()

    #while CheckCondition(probabilities) is False:
        # calculate gain and find the next test to run

        # run the test

        # modify probabilities based on test result

    
    # return the elements with probability 1

# Extract the lines from file and stores them in a dictionary
def extract_lines(file_name):
    initial_probability = 0.25
    elements = dict()
    f = open(file_name, "r")
    id = 0
    for line in f:
        elements[line] = [1, initial_probability, id]
        id += 1

    f.close()
    return elements

# Writes the reduced code with lines whose xi == 1
def write_reduced(file_name, elements):
    f = open(file_name, "w")
    for e in elements:
        if elements[e][0]:
            f.write(e)
    f.close()

def execute_reduced(file_name):
    output = subprocess.run(["python3", file_name], capture_output=True, text=True)
    # 0 == no errors, 1 == division error
    return output.returncode

def check_minimality(elements):
    for e in elements:
        if elements[e][1] != 0 and elements[e][1] != 1:
            return 0
    return 1


def probDD():
    # write a test function to invoke python3 on "test{#i}_reduction.py" and check for divisionByZero
    # generate tests
    number_tests = 3
    generate_test(number_tests)

    # for each test:
    for i in range(1, number_tests + 1):
        original_name = "test/test" + str(i) + ".py"
        reduced_name = "test/test" + str(i) + "_reduction.py"

        # 1. extract lines from the file as sequence
        elements = extract_lines(original_name)

        while True:
            print(elements)
            # 2. check 1-minimality
            if check_minimality(elements):
                break
            
            # 3. write the reduced test
            write_reduced(reduced_name, elements)
            
            # 4. execute the reduced test
            result = execute_reduced(reduced_name)
            
            # 5. adjust the probabilities according the reduced program's result (T or F)
            AdjustProbs(elements, result)

            # 6. randomize the order of the elements and sort by probability
            elements = randomize_sort(elements)

            # 7. find the next subsequence (through maximum gain)
            elements = max_gain(elements)

probDD()
#execute_reduced("test/test1_reduction.py")
#execute_reduced("test/test2_reduction.py")
#execute_reduced("test/test3_reduction.py")
