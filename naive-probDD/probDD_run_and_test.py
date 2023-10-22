import subprocess
from test.generate_random_test import generate_test

# "elements" is the list of elements to be reduced.
# "targets" is the list of element indices that are excluded subsequence.
# "result" is the test outcome if it satisfied the test or not with exclusion.
def AdjustProbs(elements, targets, result):

    if result == 1:
        for i in targets:
            elements[i][0] = 0
            elements[i][1] = 0
    elif result == 0:
        product = 1.0
        for j in targets:
            product *= ((1.0-elements[j][1]))
        for i in targets:
            if elements[i][0] == 0:
                continue
            elements[i][1] /= (1 - product)

def probDD(sequence, test_function):
    # probabilities of each element in the optimal solution
    probabilities = sequence.copy()
    # current optimal solution
    next_test_sequence = sequence.copy()

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
    for line in f:
        elements[line] = [1, initial_probability]
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

def test():
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

        #while True:
        # 2. write the reduced test
        write_reduced(reduced_name, elements)
        
        # 3. execute the reduced test
        if execute_reduced(reduced_name):
            # there was an error (T), so we try to find maximum gain
            # but first we check 1-minimality
        else:
            # there was no error (F), so we use the compliment? 


        # 4. call AdjustProb based on result of step 3
        # 5. go back to step 2
        # 6. check the final "test{#i}_reduction.py" and check minimality

test()
#execute_reduced("test/test1_reduction.py")
#execute_reduced("test/test2_reduction.py")
#execute_reduced("test/test3_reduction.py")