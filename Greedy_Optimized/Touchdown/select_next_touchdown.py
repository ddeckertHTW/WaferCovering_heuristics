import datetime
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

    #THIS CAN BE PERFORMANCE DEGRADING. Cause: Too many to dominate Dies cause the amount of checking to explode. 
    #Avoid by directly using dominated Dies and remove them from forced_dominante_map
    # Dominate Map
    if (dominante_max_val >= 1):
        dominatedDies = np.argwhere(solutionObj.forced_dominante_map == dominante_max_val)

        #Find the Best Score of all possible Touchdowns, that cover Dominated Dies
        curr_bestOptions = get_best_dominating_td_option_coords(waferMapObj, solutionObj, dominatedDies)

        #print("Dominate took time: ", datetime.datetime.now() - local_start_time)
        randomElement = curr_bestOptions[random.randint(0, len(curr_bestOptions) - 1)]
        return randomElement.x, randomElement.y
    
    #LeastFlexible Value
    if(least_Flex_max_val >= 1):
        leastFlexDies = np.argwhere(solutionObj.forced_leastFlex_map == least_Flex_max_val)
        randomElement = leastFlexDies[random.randint(0, len(leastFlexDies) - 1)]
        #AFter selecting a random element of best Value -> Get the coordinate of the touchdown
        randomElement_x, randomElement_y = get_only_least_flex_option(randomElement[0],randomElement[1], waferMapObj, solutionObj)
        #print("Choosing LeastFlex TOuchdown Option: ", least_Flex_max_val)
        return randomElement_x, randomElement_y
    

    
    #Get a List of all "Best" Options for next Touchdown.
    rating_max = np.max(solutionObj.ratings_map)
    maxRatingList = np.argwhere(solutionObj.ratings_map == rating_max)

    #print("Chossing Rating TD. Max Rating:", ratting_max)
    return maxRatingList[random.randint(0, len(maxRatingList) - 1)]  # randomElement[0] == x randomElement[1] == y


# LeastFLex == Domiante
    """
    if(least_Flex_max_val >= 1 and dominante_max_val >= 1):
        dominatedDies = np.argwhere(solutionObj.forced_dominante_map == dominante_max_val)
        leastFlexDies = np.argwhere(solutionObj.forced_leastFlex_map == least_Flex_max_val)

        labeled_dominated = [(index, 'dominated') for index in dominatedDies]
        labeled_leastFlex = [(index, 'leastFlex') for index in leastFlexDies]

        combined_dominated = labeled_dominated + labeled_leastFlex
        random_choice = random.choice(combined_dominated)
        source_list, funcName = random_choice

        if funcName == 'dominated':
            dominatedDies = np.argwhere(solutionObj.forced_dominante_map == dominante_max_val)

            #Find the Best Score of all possible Touchdowns, that cover Dominated Dies
            curr_bestOptions = get_best_dominating_td_option_coords(waferMapObj, solutionObj, dominatedDies)

            #print("Dominate took time: ", datetime.datetime.now() - local_start_time)
            randomElement = curr_bestOptions[random.randint(0, len(curr_bestOptions) - 1)]
            return randomElement.x, randomElement.y
        
        if funcName == "leastFlex":
            dominatedDies = np.argwhere(solutionObj.forced_leastFlex_map == least_Flex_max_val)
            randomElement = dominatedDies[random.randint(0, len(dominatedDies) - 1)]
            #AFter selecting a random element of best Value -> Get the coordinate of the touchdown
            dominate_x, dominate_y = get_only_least_flex_option(randomElement[0],randomElement[1], waferMapObj, solutionObj)
            #print("Choosing LeastFlex TOuchdown Option: ", least_Flex_max_val)
            return dominate_x, dominate_y
    """
    