import random
import numpy as np
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Touchdown.get_best_dominating_td_option import get_best_dominating_td_option_coords
from Greedy_Optimized.Touchdown.get_only_least_flex_option import get_only_least_flex_option


def select_next_touchdown(solutionObj: SolutionMapClass, waferMapObj: WaferMapClass):
    #First check forced optionMap, as it superseads ratings. Default value is 0
    dominante_max_val = np.max(solutionObj.forced_dominante_map)
    least_Flex_max_val = np.max(solutionObj.forced_leastFlex_map)

    bestTds = {}
    #Dominaz Value
    if (dominante_max_val >= 1):
        dominatedDies = np.argwhere(solutionObj.forced_dominante_map == dominante_max_val)
        #Find the Best Score of all Dominate Options
        best_Options = {}
        for coords in dominatedDies:
            curr_bestOptions = get_best_dominating_td_option_coords(coords[0], coords[1], waferMapObj, solutionObj, dominatedDies)
            
            #Add all best Elements to the Options
            for option in curr_bestOptions:
                best_Options[option] = (solutionObj.dieMap[option[0]][option[1]].score_gain)

        #Get the number of DOMINATED Dies this Touchdown would cover. The More dominate are covered the better...
        #td_Dies: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_1)


        #Select the best actual Touchdown to cover the Dominate Option
        max_value = max(best_Options.values())
        max_keys = [key for key, value in best_Options.items() if value == max_value]

        randomElement = max_keys[random.randint(0, len(max_keys) - 1)]
        return randomElement[0], randomElement[1]
        """ # Old Approach completely ignores the actual Value of selected TD. 
        randomElement = forcedOptions[random.randint(0, len(forcedOptions) - 1)]
        #AFter selecting a random element of best Value -> Get the coordinate of the touchdown
        dominate_x, dominate_y = get_best_dominating_td_option_coords(randomElement[0],randomElement[1], waferMapObj, solutionObj)
        #print("Choosing Dominate TOuchdown Option: ", dominante_max_val)

        return dominate_x, dominate_y"""
    
    #LeastFlexible Value
    if(least_Flex_max_val >= 1):
        dominatedDies = np.argwhere(solutionObj.forced_leastFlex_map == least_Flex_max_val)
        randomElement = dominatedDies[random.randint(0, len(dominatedDies) - 1)]
        #AFter selecting a random element of best Value -> Get the coordinate of the touchdown
        dominate_x, dominate_y = get_only_least_flex_option(randomElement[0],randomElement[1], waferMapObj, solutionObj)
        #print("Choosing LeastFlex TOuchdown Option: ", least_Flex_max_val)
        return dominate_x, dominate_y


    #Get a List of all "Best" Options for next Touchdown.
    rating_max = np.max(solutionObj.ratings_map)
    maxRatingList = np.argwhere(solutionObj.ratings_map == rating_max)

    #print("Chossing Rating TD. Max Rating:", ratting_max)
    return maxRatingList[random.randint(0, len(maxRatingList) - 1)]  # randomElement[0] == x randomElement[1] == y



"""

def select_next_touchdown(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    bin_list = solutionObj.dieMap.flatten()

    #The Coordinates here show which bin has only one way to be covered. NOT the Touchdown Pos TO cover this one bin.
    if any(bin.dominate > 1 for bin in bin_list):
        max_value_dominate = max(obj.dominate for obj in bin_list)
        dominate_list = [obj for obj in bin_list if obj.dominate == max_value_dominate]
        randomElement = dominate_list[random.randint(0, len(dominate_list) - 1)]  
        return randomElement.x, randomElement.y 

    #LeastFlexible Dies werden IMMER genommen
    if solutionObj.skip_least_flexible == False and any(bin.least_flexible == 1 for bin in bin_list):
        least_flexible_list = [obj for obj in bin_list if obj.least_flexible == 1]

        randomElement = least_flexible_list[random.randint(0, len(least_flexible_list) - 1)]  
        return get_only_least_flex_option(randomElement.x, randomElement.y, waferMapObj, solutionObj)

    #Otherwise Pick the highest Score
    max_value_score = max(obj.score_gain for obj in bin_list)
    score_gain_list = [obj for obj in bin_list if obj.score_gain == max_value_score]
    randomElement = score_gain_list[random.randint(0, len(score_gain_list) - 1)]

    return randomElement.x, randomElement.y  # randomElement[0] == x randomElement[1] == y
"""