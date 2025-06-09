from typing import List
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.NPMaskOperations.get_coordinates_by_mask import get_coordinates_by_mask
from Greedy_Optimized.NPMaskOperations.get_values_by_coord_list import get_values_by_coord_list
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Touchdown.get_touchdown_options_to_cover_die import get_touchdown_options_to_cover_die

#TODO:
# Find alFind all Touchdowns that cover the Max amount of dominated Dies. 
# Then compare the scores of these Options and return all touchdown coordinates (list) for Touchdowns with the best score.

# When a die cannot be coverd without creating a double TD -> Better find the best possibilitys to cover it NOW. to avoid more doubles later
# Returns x,y Value of the "best" Option
def get_best_dominating_td_option_coords(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, dominatedDies): 
    #First get all Unique Touchdowns, that would cover ANY of the dominated Dies at once (to avoid multiple calculations of the same Die)
    touchdown_options_unique = set()  
    for dominatedDie in dominatedDies:
        touchdown_options_unique.update(get_touchdown_options_to_cover_die(dominatedDie[0], dominatedDie[1] ,waferMapObj))

    best_Options = {}
    #Check which options cover the most amount of dominated Dies
    for option_coord in touchdown_options_unique:
        #TD Must be possible
        if(solutionObj.dieMap[option_coord[0], option_coord[1]].td_possible_as_site1 == False):
            continue

        #Count how many to Dominate Dies are covered by the current Touchdown
        option_touchedCoords: List[DieClass] = get_coordinates_by_mask(option_coord[0], option_coord[1], solutionObj.dieMap, waferMapObj.probecard.mask_1)
        domiated_Die_Touched_count = sum(1 for element in dominatedDies if tuple(element) in option_touchedCoords)
        
        #best_Options[domiated_Die_Touched_count] = option
        # Add the coordinate Option to a list of elements in the dict. Key is the countof dominated Dies it coveres 
        if domiated_Die_Touched_count in best_Options:
            best_Options[domiated_Die_Touched_count].append(option_coord)
        else:
            best_Options[domiated_Die_Touched_count] = [option_coord]

    # Just look at the "best" highest count of dominated Dies
    maxOptions = best_Options[max(best_Options)]
    best_Dies = get_values_by_coord_list(solutionObj.dieMap, maxOptions)

    # Find the Max Score and then return a list of all Coordinates that have THIS Score in the  
    max_score = max(best_Dies, key=lambda elem: elem.score_gain).score_gain
    max_score_Dies = [elem for elem in best_Dies if elem.score_gain == max_score]

    #Example: [(7, 7), (6, 7), (5, 7)]
    return max_score_Dies


"""
# When a die cannot be coverd without creating a double TD -> Better find the best possibilitys to cover it NOW. to avoid more doubles later
# Returns x,y Value of the "best" Option
def get_best_dominating_td_option_coords(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, dominatedDies): 
    #All Objects that could cover the Bin we want to cover (with double td)
    td_options = get_touchdown_options_to_cover_die(x, y ,waferMapObj)

    best_Options = {}
    #Check which options cover the most amount of dominated Dies
    for option_coord in td_options:
        #TD Must be possible
        if(solutionObj.dieMap[option_coord[0], option_coord[1]].td_possible_as_site1 == False):
            continue

        #Count how many to Dominate Dies are covered by the current Touchdown
        option_touchedCoords: List[DieClass] = get_coordinates_by_mask(option_coord[0], option_coord[1], solutionObj.dieMap, waferMapObj.probecard.mask_1)
        domiated_Die_Touched_count = sum(1 for element in dominatedDies if tuple(element) in option_touchedCoords)
        
        #best_Options[domiated_Die_Touched_count] = option
        # Add the coordinate Option to a list of elements in the dict. Key is the countof dominated Dies it coveres 
        if domiated_Die_Touched_count in best_Options:
            best_Options[domiated_Die_Touched_count].append(option_coord)
        else:
            best_Options[domiated_Die_Touched_count] = [option_coord]

    # Just look at the "best" highest count of dominated Dies
    maxOptions = best_Options[max(best_Options)]
    best_Dies = get_values_by_coord_list(solutionObj.dieMap, maxOptions)

    # Find the Max Score and then return a list of all Coordinates that have THIS Score in the  
    max_score = max(best_Dies, key=lambda elem: elem.score_gain).score_gain
    max_score_Elems = [(elem.x, elem.y) for elem in best_Dies if elem.score_gain == max_score]

    #Example: [(7, 7), (6, 7), (5, 7)]
    return max_score_Elems


"""