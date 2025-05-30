from typing import List

import numpy as np
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE
from Greedy_Optimized.NPMaskOperations.get_values_by_coord_list import get_values_by_coord_list
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

"""
Range of Values for all Variables:
score_gain - MAX VALUE IS BEST
    -Max: 1 * SiteCount
    -Min: -inf

adjacent_flex_sum:  - MIN VALUE IS BEST
    -Max: SiteCount * SiteCount           sum(die.least_flexible for die in adjacent_Sum)
    -Min: 0

border_possibilities_static - MIN VALUE IS BEST
    -Max: SiteCount * SiteCount   
    -Min: 0
"""

#TODO:
weight_score_gain = 1
#weight_adjacent_flex_sum = 1
#weight_border_possibilities_static = 1

# After updating DieMap Values -> combine them to ratings_map and forced_options_map - from which the next touchdown decision can be made 
def update_decision_variables(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    die_list: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_4) #ALL updated Dies
    #TODO: Loop adjacent Rating only over this and not ALL elements. MASK 3 would be way less computing. 
    #Adjacent_die_list: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_6)
    
    update_decision_variables_by_List(die_list,waferMapObj, solutionObj)

#Make it uniform from init to update on the fly
def update_decision_variables_by_List(die_list: List[DieClass], waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    for die in die_list:
        ratingOption = 0
        #If Touchdown is not possible at all -> SET SKIP FLAG
        if(solutionObj.dieMap[die.x][die.y].td_possible_as_site1 == False or
            solutionObj.dieMap[die.x][die.y].score_gain == IMPOSSIBLE_VALUE_NEGATIVE):
            ratingOption = IMPOSSIBLE_VALUE_NEGATIVE
        else:
            #Baseline of the Rating is the Score. Current Weight:
            ratingOption += weight_score_gain * solutionObj.dieMap[die.x][die.y].score_gain

            # So MAX Value is probecard.size*probecard.size (maxSitesSum)
            #Adjacent MUST be a buff, because only a few elements get it
            if(solutionObj.dieMap[die.x][die.y].adjacent_flex_sum > 0):
                #THIS Version prioritizes, to NOT leave single DIes untouched, but may only place a TD, that covers 1 DIe. WAY MORE TDs (As it USES ALL SPACE)
                #ratingOption += -(solutionObj.dieMap[die.x][die.y].adjacent_flex_sum)
                #THIS Version will take more of the "best" score but may lead to more double TDs. More Focused Solutions
                ratingOption += -(solutionObj.dieMap[die.x][die.y].adjacent_flex_sum / waferMapObj.probecard.sitesCount) * 1.5

                #print(f"{die.x} {die.y} | Gain: {solutionObj.dieMap[die.x][die.y].score_gain} | Adjacent Minus: {(solutionObj.dieMap[die.x][die.y].adjacent_flex_sum / waferMapObj.probecard.sitesCount)} | Final rating: {ratingOption} | AND Border: {solutionObj.dieMap[die.x][die.y].border_possibilities_static / waferMapObj.probecard.sitesCount}")
            else:   # Else minus THE MAXIMUM possible Val
                ratingOption += -(waferMapObj.probecard.maxSitesSum)
                #print(f"{die.x} {die.y} | Gain: {solutionObj.dieMap[die.x][die.y].score_gain} | Adjacent Max Minus: {(waferMapObj.probecard.maxSitesSum)} | Final rating: {ratingOption}")

            #Idea: Only care for Border Buff, when desciding about adjacent???
            #This Version is prioritizing Border Elements VERY Much
            #ratingOption += -(solutionObj.dieMap[die.x][die.y].border_possibilities_static)
            #THis Version is scaled down to match rating Max
            #ratingOption += -(solutionObj.dieMap[die.x][die.y].border_possibilities_static / waferMapObj.probecard.sitesCount)

            #print(f"{die.x} {die.y} | Border: {solutionObj.dieMap[die.x][die.y].border_possibilities_static} | Border Calc: {solutionObj.dieMap[die.x][die.y].border_possibilities_static / waferMapObj.probecard.sitesCount}")
        
        #print(f"Rating : {ratingOption}, Score: {solutionObj.dieMap[die.x][die.y].score_gain}, Adjacent: {solutionObj.dieMap[die.x][die.y].adjacent_flex_sum}, Border: {solutionObj.dieMap[die.x][die.y].border_possibilities_static}")

        # Score, Adjacent, Border etc. combined
        solutionObj.ratings_map[die.x][die.y] = ratingOption

        #print(f"{die.x} {die.y} | \tScore: {solutionObj.dieMap[die.x][die.y].score_gain}," +
        #      f"\tAdjacent: {solutionObj.dieMap[die.x][die.y].adjacent_flex_sum}, AdjCalc: {solutionObj.dieMap[die.x][die.y].adjacent_flex_sum / waferMapObj.probecard.sitesCount}, ElseVal: {waferMapObj.probecard.maxSitesSum} " + 
        #      f"\tBorder:{solutionObj.dieMap[die.x][die.y].border_possibilities_static}. BorderCalc: {solutionObj.dieMap[die.x][die.y].border_possibilities_static / waferMapObj.probecard.sitesCount} | " + 
        #      f"Td: Value {solutionObj.dieMap[die.x][die.y].touchdown}, Final Rating: {ratingOption} ")

        #TODO: What is the max/min possible Value of RATING????? 

        # Dominate > leastFlex currently. They excude each other. Should not be possible for both attributes be present in one die
        if die.dominate == 1:
            solutionObj.forced_dominante_map[die.x][die.y] = 2
            #If we want to calculate the coordinate of the DOminating TOuchdown of this Die -> But has other Problems with updating
            #dominate_x, dominate_y = get_best_dominating_td_option(die.x,die.y, waferMapObj, solutionObj)
            #solutionObj.forced_dominante_map[dominate_x][dominate_y] = 2
            
            #IDEA: Instead of PURE Random. ADD be rating VALUE instead?? 
            # THIS CAN BE BAD, because We want to choose a hurtfull Option and choosing the least hurtfull may not cover ALL troubled Tds
            #TODO: WARNING. THIS IS FAULTY. DEPENDING ON UPDATE ORDER A OLD AND NEW RANKING ARE MIXED
            """best_x, best_y = get_best_dominating_td_option_coords(die.x, die.y, waferMapObj, solutionObj)
            bestValue = solutionObj.ratings_map[best_x][best_y]

            normalized_Rating = normalize_Value(bestValue, -waferMapObj.probecard.maxSitesSum * 2, waferMapObj.probecard.maxSitesSum * 2)
            print(f"Val: {bestValue}, Normalized: {normalized_Rating}")
            solutionObj.forced_dominante_map[die.x][die.y] += normalized_Rating"""
        else:
            solutionObj.forced_dominante_map[die.x][die.y] = 0


        if die.least_flexible == 1:
            solutionObj.forced_leastFlex_map[die.x][die.y] = 2
            #If we want to calculate the coordinate of the DOminating TOuchdown of this Die -> But has other Problems with updating
            #least_x, least_y = get_only_least_flex_option(die.x,die.y, waferMapObj, solutionObj)
            #solutionObj.forced_leastFlex_map[least_x][least_y] = 1
            
            #IDEA: Instead of PURE Random. ADD be rating VALUE instead?? 
            # THIS CAN BE BAD, because We want to choose a hurtfull Option and choosing the least hurtfull may not cover ALL troubled Tds
            #TODO: WARNING. THIS IS FAULTY. DEPENDING ON UPDATE ORDER A OLD AND NEW RANKING ARE MIXED
            """best_x, best_y = get_only_least_flex_option(die.x, die.y, waferMapObj, solutionObj)
            bestValue = solutionObj.ratings_map[best_x][best_y]

            normalized_Rating = normalize_Value(bestValue, -waferMapObj.probecard.maxSitesSum * 2, waferMapObj.probecard.maxSitesSum * 2)
            print(f"Val: {bestValue}, Normalized: {normalized_Rating}")
            solutionObj.forced_leastFlex_map[die.x][die.y] += normalized_Rating"""

        else:
            solutionObj.forced_leastFlex_map[die.x][die.y] = 0
    

def update_decision_variables_init(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    all_possible_dies = get_values_by_coord_list(solutionObj.dieMap, waferMapObj.get_all_Possible_Touchdowns())
   
    update_decision_variables_by_List(all_possible_dies,waferMapObj, solutionObj)

#Scale Value down: -1 to +1 
def normalize_Value(value, min_value, max_value):
    if value == IMPOSSIBLE_VALUE_NEGATIVE:
        return -1
    
    normalized_value = (value - min_value) / (max_value - min_value)
    scaled_value = 2 * normalized_value - 1
    return scaled_value
