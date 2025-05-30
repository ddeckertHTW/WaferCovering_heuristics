from typing import List

import numpy as np
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE, PENALTY_SCORE
from Greedy_Optimized.NPMaskOperations.get_values_by_coord_list import get_values_by_coord_list
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

"""
Range of Values for all Variables:
score_gain - MAX VALUE IS BEST
    -Max: PENALTY_SCORE * SiteCount
    -Min: -inf
    -Min Realistic Threshold: -(PENALTY_SCORE^2 * SiteCount) -> Alle Touchdowns sind doppelte TDs (2^2 = 4)

adjacent_flex_sum:  - MIN VALUE IS BEST
    -Max: SiteCount * SiteCount           sum(die.least_flexible for die in adjacent_Sum)
    -Min: 0

optional_covered_buff_static - Max Value is best
    -Max: SiteCount - 1 #Atleast one Must Touch Die must be covered
    -Min: 0

forbidden_distance_static - MIN VALUE IS BEST
    -Max: inf   
    -Min: 1 # Cannot be ontop of a forbidden die.
"""



# After updating DieMap Values -> combine them to ratings_map and forced_options_map - from which the next touchdown decision can be made 
def update_decision_variables(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    die_list: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_4) #ALL updated Dies
    #TODO: Loop adjacent Rating only over this and not ALL elements. MASK 3 would be way less computing. 
    #Adjacent_die_list: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_6)
    
    update_decision_variables_by_List(die_list,waferMapObj, solutionObj)

#Make it uniform from init to update on the fly
def update_decision_variables_by_List(die_list: List[DieClass], waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    for die in die_list:
        if(solutionObj.dieMap[die.x][die.y].td_possible_as_site1 == False):
            solutionObj.ratings_map[die.x][die.y] = IMPOSSIBLE_VALUE_NEGATIVE
            solutionObj.forced_dominante_map[die.x][die.y] = 0
            solutionObj.forced_leastFlex_map[die.x][die.y] = 0


        ratingOption = 0
        #If Touchdown is not possible at all -> SET SKIP FLAG
        if(solutionObj.dieMap[die.x][die.y].score_gain == IMPOSSIBLE_VALUE_NEGATIVE):
            ratingOption = IMPOSSIBLE_VALUE_NEGATIVE
        else:
            #Baseline of the Rating is the Score. Current Weight:
            #ratingOption = solutionObj.dieMap[die.x][die.y].score_gain

            #Normalize
            score_normalized = normalize_asynchrone(value = solutionObj.dieMap[die.x][die.y].score_gain, max = PENALTY_SCORE * waferMapObj.probecard.sitesCount, minThreshold = -pow(PENALTY_SCORE, 2) * waferMapObj.probecard.sitesCount )
            #print(f"Score:  \t{round(solutionObj.dieMap[die.x][die.y].score_gain, 1)} \t Normalized: {round(score_normalized, 1)}")

            #CAREFULL. BEST VALUE IS NEAR 0. WORST IS INF. Thats why 1 - normalize_min_max
            if solutionObj.dieMap[die.x][die.y].adjacent_flex_sum == IMPOSSIBLE_VALUE_POSITIVE:
                adjacent_normalized = 0
            else:
                adjacent_normalized = 1 - normalize_min_max(solutionObj.dieMap[die.x][die.y].adjacent_flex_sum, max = waferMapObj.probecard.sitesCount * waferMapObj.probecard.sitesCount, min = 0)
                #print(f"adjacent:\t{round(solutionObj.dieMap[die.x][die.y].adjacent_flex_sum, 1)} \t Normalized: {round(adjacent_normalized, 1)}")


            # BOTH THESE VARIABLES GET COMBINED INTO ONE: forbidden_distance_and_optional_covered_static
            optional_buff_normalized = normalize_min_max(solutionObj.dieMap[die.x][die.y].optional_covered_buff_static, max = waferMapObj.probecard.sitesCount - 1, min = 0)
            #print(f"optional:\t{round(solutionObj.dieMap[die.x][die.y].optional_covered_buff_static, 1)} \t Normalized: {round(optional_buff_normalized, 1)}")

            forbidden_distance_normalized = normalize_zero_to_inf(solutionObj.dieMap[die.x][die.y].forbidden_distance_static, 1)
            #print(f"forbidden:\t{round(solutionObj.dieMap[die.x][die.y].forbidden_distance_static, 1)} \t Normalized: {round(forbidden_distance_normalized, 1)}")

            #Both get 50:50 Influence
            optional_normalized_variables = optional_buff_normalized * 0.5 + forbidden_distance_normalized * 0.5

            weighted_normalized_vals = 0
            if waferMapObj.weightSettingsObj is None:
                weighted_normalized_vals = (1 * score_normalized)
            else:
                weighted_normalized_vals = ((waferMapObj.weightSettingsObj.weight_score_gain * score_normalized) + 
                                        (waferMapObj.weightSettingsObj.weight_adjacent_flex_sum * adjacent_normalized) + 
                                        (waferMapObj.weightSettingsObj.weight_forbidden_distance_and_optional_covered_static * optional_normalized_variables))
            #print("Total weighted_normalized_vals:", weighted_normalized_vals)
            
            ratingOption = weighted_normalized_vals
        
        # Score, Adjacent, Border etc. combined
        solutionObj.ratings_map[die.x][die.y] = ratingOption

        # Dominate > leastFlex currently. They excude each other. Should not be possible for both attributes be present in one die
        if die.dominate == 1:
            solutionObj.forced_dominante_map[die.x][die.y] = 2
        else:
            solutionObj.forced_dominante_map[die.x][die.y] = 0

        #Least Flexible
        if die.least_flexible == 1:
            solutionObj.forced_leastFlex_map[die.x][die.y] = 2
        else:
            solutionObj.forced_leastFlex_map[die.x][die.y] = 0
    

def update_decision_variables_init(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    all_possible_dies = get_values_by_coord_list(solutionObj.dieMap, waferMapObj.get_all_Possible_Touchdowns())
   
    update_decision_variables_by_List(all_possible_dies,waferMapObj, solutionObj)

# Taking Max value 0 to 1 from Value 0 to Max
# Taking Value 0 to -minThreshold and create a half negative scaling between 0 to -0.5
# Value under -0.5 get Scaled to inf to the Value -1
def normalize_asynchrone(value, max, minThreshold):
    if value >= 0:
        # Positive range, normalize between 0 and 1
        return value / max
    elif value >= minThreshold:
        return - (value / (minThreshold * 2)) #Offset as we only want Values from 0 to -0.5
    else:
        # lim -> -inf. The closer the value is to -inf the closer it gets to value -1
        return ((value - minThreshold/2) / (abs(value) + 1))

""" EXAMPLE DATA normalize_asynchrone
MAX = 10, MinTHreshhold = -5
val:  10  Normalized:  1.0
val:  5  Normalized:  0.5
val:  0  Normalized:  0.0
val:  -1  Normalized:  -0.1
val:  -3  Normalized:  -0.3
val:  -4  Normalized:  -0.4
val:  -5  Normalized:  -0.5
val:  -6  Normalized:  -0.5
val:  -7  Normalized:  -0.5625
val:  -10  Normalized:  -0.6818181818181818
val:  -100  Normalized:  -0.9653465346534653
val:  -999999  Normalized:  -0.9999965
"""

#Just a Basic Return Value of 0 to 1. Between MaxVal and minVal 
def normalize_min_max(value, max, min):
    normalized_value = (value - min) / (max - min)
    return normalized_value

""" normalize_min_max
MAX = 10, MIN = 0
val:  10  Normalized:  1.0
val:  8  Normalized:  0.8
val:  5  Normalized:  0.5
val:  1  Normalized:  0.1
val:  0  Normalized:  0.0
"""

# Normalize. Besst Value is 0 and Worst is +inf
def normalize_zero_to_inf(value, max):
    if value == 0:
        return None
    return max / value
""" normalize_zero_to_inf
MAX = 1
val:  1000  Normalized:  0.001
val:  100  Normalized:  0.01
val:  10  Normalized:  0.1
val:  8  Normalized:  0.125
val:  5  Normalized:  0.2
val:  1  Normalized:  1.0
"""


#Normalize with MAX val and min Value -inf. 
# Returns Value 1 to -1 (IS BAD BECAUSE -1 == -0.5 Value)
#def normalize_max_to_minInf(value, max):
#    if value >= 0:
#        # Positive range, normalize between 0 and 1
#        return value / max
#    else:
#        # lim -> -inf. The closer the value is to -inf the closer it gets to value -1
#        return (value / (abs(value) + 1))
""" normalize_max_to_minInf
MAX = 10
val:  10  Normalized:  1.0
val:  5  Normalized:  0.5
val:  0  Normalized:  0.0
val:  -1  Normalized:  -0.5
val:  -3  Normalized:  -0.75
val:  -4  Normalized:  -0.8
val:  -5  Normalized:  -0.8333333333333334
val:  -6  Normalized:  -0.8571428571428571
val:  -7  Normalized:  -0.875
val:  -10  Normalized:  -0.9090909090909091
val:  -100  Normalized:  -0.9900990099009901
val:  -999999  Normalized:  -0.999999
"""