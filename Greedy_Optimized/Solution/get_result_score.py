# Zielfunktion ist S^tdc(d). S angenommen 2
from GlobalConstants import PENALTY_SCORE

#Input dict: {1: 224, 2: 32} -> Result is a int score
def get_result_score(rating_dict):
    score = 0
    for key, key_count in rating_dict.items():
        # KEY - 1 ist INTUITIVER VON DEN WERTEN!!!!
        # Aber Mathematische Def mit oder ohne -1???
        score += pow(PENALTY_SCORE, key) * key_count
        #print(f"Key:{key}, Count: {key_count} - Score: {pow(PENALTY_SCORE, key - 1)} * {key_count} = {pow(PENALTY_SCORE, key - 1) * key_count} | currSum = {score}")

    return score