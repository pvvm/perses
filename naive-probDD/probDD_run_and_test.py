def probDD(sequence, test_function):
    # probabilities of each element in the optimal solution
    probabilities = sequence.copy()
    # current optimal solution
    next_test_sequence = sequence.copy()

    while ...:
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