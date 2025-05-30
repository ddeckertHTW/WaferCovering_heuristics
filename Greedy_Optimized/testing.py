import itertools

values = [0.1, 0.5, 1, 1.5, 2]
values = [1, 2, 4]
combinations = list(itertools.product(values, repeat=2))

# Function to normalize combinations by their ratio
def normalize_ratio(pair):
    a, b = pair
    # Ensure we don't divide by zero
    if b != 0:
        ratio = a / b
    else:
        ratio = float('inf')  # Handle case when denominator is zero
    return ratio

# Store ratios that we've seen
unique_combinations = []
thrown_away_combinations = []
seen_ratios = set()

for combo in combinations:
    ratio = normalize_ratio(combo)
    #inverse_ratio = normalize_ratio(combo[::-1])  # For the inverse ratio (b/a)
    
    # If neither the ratio nor its inverse has been seen, add to unique combinations
    if ratio not in seen_ratios: # and inverse_ratio not in seen_ratios:
        unique_combinations.append(combo)
        seen_ratios.add(ratio)
    else:
        thrown_away_combinations.append(combo)


print("Total number of combinations:", len(combinations))
print("Total number of UNIQUE combinations:", len(unique_combinations))

print("Unique: ",unique_combinations)
print("BAD: ",thrown_away_combinations)
