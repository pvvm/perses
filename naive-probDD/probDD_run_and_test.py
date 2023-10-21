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

    while CheckCondition(probabilities) is False:
        # calculate gain and find the next test to run

        # run the test

        # modify probabilities based on test result

    
    # return the elements with probability 1


def test():
    # write a test function to invoke python3 on "test{#i}_reduction.py" and check for divisionByZero
    # generate tests
    # for each test:
    # 1. extract lines from the file as sequence
    # 2. find a smaller test
    # 3. call the test function, it should generate "test{#i}_reduction.py" and invoke python3
    # 4. call AdjustProb based on result of step 3
    # 5. go back to step 2
    # 6. check the final "test{#i}_reduction.py" and check minimality