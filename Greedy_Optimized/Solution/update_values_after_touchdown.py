#Update PlacementOptions abd Rating here 
from typing import List
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Solution.get_least_flexible_tdMap import get_least_flexible_tdMap
from Greedy_Optimized.Solution.get_td_score_gain import get_td_score_gain
from Greedy_Optimized.Touchdown.is_touchdown_creating_doubleTd import is_touchdown_creating_doubleTd

#dieList: List[DieClass]

def update_values_after_touchdown(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    #The Touchdown Site1 Cannot be used again...
    solutionObj.ratings_map[x][y] = IMPOSSIBLE_VALUE_NEGATIVE

    #The Touchdown Dies that were just placed -> Reset all Values that depend on not creating double TDs
    td_Dies: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_1)
    for die in td_Dies:
        #No DoubleTD allowed
        die.least_flexible = 0

        # If a dominated Dies was touched -> most likely "used" in decision for this TD -> Reset 
        die.dominate = 0 

        # RESET decision MAP Values aswell
        solutionObj.forced_leastFlex_map[die.x][die.y] = 0 #IMPOSSIBLE_VALUE_NEGATIVE
        solutionObj.forced_dominante_map[die.x][die.y] = 0 #IMPOSSIBLE_VALUE_NEGATIVE

        #UPDATE Score of Dies aswell. X/Y of touchdown will be IMPOSSIBLE_VALUE_NEGATIVE
        die.score_gain = get_td_score_gain(die.x, die.y, waferMapObj, solutionObj)

        #Adjacent must be reset as it would create Double TD 
        die.adjacent_flex_sum = IMPOSSIBLE_VALUE_POSITIVE


    # LeastFlex Map of the local mask_4 WaferMap. If no leastFlex Elements. will return a empty Map full of 0
    leastFlexTdMap = get_least_flexible_tdMap(x, y, waferMapObj, solutionObj) 
    
    #Update Area Without INNER TouchdownArea
    #Get all affected dies where Values should Change. WITHOUT the inner current Touchdown -> mask5 
    die_list_mask5: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_5)
    for die in die_list_mask5:
        die.score_gain = get_td_score_gain(die.x, die.y, waferMapObj, solutionObj)

        # Workaround to update Dominate Dies GLOBALLY.
        # DOminate is basicly all Dies, that must be covered but cannot be by the current leastFlex Map
        #print(die.x, die.y, (die.is_mandatory and die.touchdown == 0 and leastFlexTdMap[die.x][die.y] == 0),die.td_possible_as_site1, die.is_mandatory, die.touchdown, leastFlexTdMap[die.x][die.y])
        if(die.is_mandatory and die.touchdown == 0 and leastFlexTdMap[die.x][die.y] == 0):
            die.dominate = 1
        else:
            die.dominate = 0

        #All Adjacent Buffs in this affected Area are no longer correct. Will be calculated later with sums.
        if(die.td_possible_as_site1):
            die.adjacent_flex_sum = IMPOSSIBLE_VALUE_POSITIVE

        #Least Flexible Dies. Calculate the whole Surrounding Map instead and assing relevant Dies hiere
        if(die.is_mandatory):
            die.least_flexible = leastFlexTdMap[die.x][die.y]


    #Look at all adjacent Dies and give them a Buff IF a touchdown is possible without creating a double td.
    die_list_mask_adjacent: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_adjacent)
    for die in die_list_mask_adjacent:
        #Abort, if TD would not be possible either way
        if(die.td_possible_as_site1 == False):
            continue

        if(is_touchdown_creating_doubleTd(die.x, die.y, waferMapObj, solutionObj) == False):
            #curr_die_list = get_values_by_mask(die.x, die.y, solutionObj.dieMap, waferMapObj.probecard.mask_1)
            adjacent_Sum = get_values_by_mask(die.x, die.y, solutionObj.dieMap, waferMapObj.probecard.mask_1)
            die.adjacent_flex_sum = sum(die.least_flexible for die in adjacent_Sum)
        else:
            die.adjacent_flex_sum = IMPOSSIBLE_VALUE_POSITIVE




