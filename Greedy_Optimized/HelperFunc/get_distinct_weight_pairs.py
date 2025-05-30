#    values = [1, 2, 4] combinations_repeat = 2
import itertools

#    values = [1, 2, 4]
def get_distinct_weight_pairs(weights, combinations_repeat):
    combinations = list(itertools.product(weights, repeat=combinations_repeat))

    # Function to normalize combinations by their ratio
    def normalize_ratio(pair):
        a, b = pair
        # Ensure we don't divide by zero
        if b != 0:
            ratio = a / b
        else:
            ratio = float('inf')  # Handle case when denominator is zero
        return ratio

    #Tripples
    def normalize_ratios_tripple(triplet):
        a, b, c = triplet
        
        # Ensure no division by zero and handle cases where b or c might be zero
        ratio_ab = a / b if b != 0 else float('inf')
        ratio_bc = b / c if c != 0 else float('inf')
        ratio_ac = a / c if c != 0 else float('inf')
        
        # Return the ratios as a tuple (this will help with comparison)
        return (ratio_ab, ratio_bc, ratio_ac)

    # Store ratios that we've seen
    unique_combinations = []
    thrown_away_combinations = []
    seen_ratios = set()

    for combo in combinations:
        if combinations_repeat == 2:
            ratio = normalize_ratio(combo)
        elif combinations_repeat == 3:
            ratio = normalize_ratios_tripple(combo)


        # If neither the ratio  has been seen, add to unique combinations
        if ratio not in seen_ratios:
            unique_combinations.append(combo)
            seen_ratios.add(ratio)
        else:
            thrown_away_combinations.append(combo)

    #print("Unique: ",unique_combinations)
    #print("BAD: ",thrown_away_combinations)

    #print("Total number of combinations:", len(combinations))
    #print("Total number of UNIQUE combinations:", len(unique_combinations))

    return unique_combinations


#######################
if __name__ == "__main__":
    weights = [0.25, 0.5, 1, 1.5, 2]
    combinations_repeat = 2 #How many permutations of these Weights should be generated

    weight_pairs = get_distinct_weight_pairs(weights, combinations_repeat)

    count = 10

    dictionary = {i+10: pair for i, pair in enumerate(weight_pairs)}


    print(dictionary)
    print("Len: ",len(dictionary))

