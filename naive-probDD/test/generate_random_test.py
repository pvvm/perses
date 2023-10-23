import random
import string
import sys

def generate_random_test(filename):
    statements = ["initialization", "print", "assignment"]
    expressions = ["identifier", "literal", "plus", "minus", "multiply"]
    test_string = ""
    current_identifiers = []
    random.seed()

    def generate_random_expression(depth):
        # depth will bound the maximum depth of the generated expression
        expression = random.choice(expressions)
        if expression == "identifier":
            if not current_identifiers:
                expression = generate_random_expression(depth)
            else:
                expression = random.choice(current_identifiers)
        elif depth == 0 or expression == "literal":
            expression = str(random.randint(0, 100))
        elif expression == "plus":
            expression = "(" + generate_random_expression(depth - 1) + "+" + generate_random_expression(depth - 1) + ")"
        elif expression == "minus":
            expression = "(" + generate_random_expression(depth - 1) + "-" + generate_random_expression(depth - 1) + ")"
        else:
            expression = "(" + generate_random_expression(depth - 1) + "*" + generate_random_expression(depth - 1) + ")"
        return expression
    
    def generate_random_statement():
        expression_depth = 5
        statement = random.choice(statements)
        if statement == "initialization":
            variable_length = random.randint(1, 10)
            def generate_random_var_name():
                return ''.join(random.choices(string.ascii_uppercase +
                                              string.ascii_lowercase, k=variable_length))
            variable = generate_random_var_name()
            while variable in current_identifiers:
                variable = generate_random_var_name()
            statement = variable + "=" + generate_random_expression(expression_depth)
            current_identifiers.append(variable)
        elif statement == "print":
            statement = "print(" + generate_random_expression(expression_depth) + ")"
        else:
            if not current_identifiers:
                random.seed()
                statement = generate_random_statement()
            else:
                variable = random.choice(current_identifiers)
                statement = variable + "=" + generate_random_expression(expression_depth)
        return statement
    
    test_length = random.randint(20, 200)
    division_by_zero_insertion_point = random.randint(0, test_length - 1)
    i = 0
    while i < test_length:
        if i == division_by_zero_insertion_point:
            # insert a division by zero
            if not current_identifiers:
                test_string += str(random.randint(0, 100)) + "/0"
            else:
                test_string += random.choice(current_identifiers) + "/0"
        else:
            test_string += generate_random_statement()
        test_string += '\n'
        i += 1
    f = open("test/" + filename, "w")
    f.write(test_string)
    f.close()

def generate_test(number):
    #args = sys.argv[1:]
    #if number != 1:
    #    print("Usage: python3 generate_random_test.py [int]")
    #else:
        #test_number = int(args[0])
    for i in range(number):
        filename = "test" + str(i+1) + ".py"
        random.seed()
        generate_random_test(filename)