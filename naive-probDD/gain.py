import random

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

    return dict(sorted(elements.items()))

def main():
    #elements = {0: [1, 0.25], 1: [1, 0.25], 2: [1, 0.25], 3: [1, 0.25], 4: [1, 0.25], 5: [1, 0.25], 6: [1, 0.25], 7: [1, 0.25]}
    elements = {0: [1, 0.3657], 1: [1, 0.3657], 2: [1, 0.3657], 3: [0, 0], 4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [1, 0.3657]}
    #elements = {0: [1, 0.6119], 1: [0, 0], 2: [1, 0.6119], 3: [0, 0], 4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [1, 0.6119]}
    #elements = {0: [0, 0], 1: [0, 0], 2: [1, 1], 3: [0, 0], 4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [1, 0.6119]}

    elements = randomize_sort(elements)
    elements = max_gain(elements)
    print(elements)


if __name__ == "__main__":
    main()