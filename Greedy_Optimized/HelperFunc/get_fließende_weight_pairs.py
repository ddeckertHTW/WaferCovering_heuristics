def generate_weight_pairs(n):
    # Generate the values from 0 to 100 in steps of 5
    values = list(range(0, 101, 5))

    # Generate all pairs (x, y) such that x + y = 100
    pairs = [(100 - x, x) for x in values]
    return pairs


def generate_weight_triples(fixed_step):
    values = list(range(0, 101, fixed_step))

    # Generate all triples (x, y, z) such that x + y + z = 100
    triples = [(x, y, 100 - x - y) for x in values for y in values if 100 - x - y in values]
    return triples

if __name__ == "__main__":
    # Example usage:
    pairs = generate_weight_pairs(20)
    for pair in pairs:
        print(pair)

    print("NOW TRIPPLES")

    # Example usage:
    triples = generate_weight_triples(10)
    for triple in triples:
        print(triple)

    #dictionary = {i+10: pair for i, pair in enumerate(pairs)}

    dictionary = {i+34: pair for i, pair in enumerate(triples)}
    print(dictionary)

    for key, value in dictionary.items():
        print(f"{key}: {value},")

    print("len Double:", len(pairs))
    print("len triple:", len(triples))