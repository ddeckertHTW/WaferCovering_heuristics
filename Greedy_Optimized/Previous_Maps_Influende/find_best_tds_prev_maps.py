import datetime
import os
import random
import sys
import numpy as np

from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Previous_Maps_Influende.prev_map_update_adjacent import prev_map_update_adjacent
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Greedy_Optimized.HelperFunc.print_colored_debug_maps import print_two_arrays
from Greedy_Optimized.Previous_Maps_Influende.prev_map_update_score import prev_map_update_score
from Greedy_Optimized.Probecard.getProbecardByName import getProbecardByName
from Greedy_Optimized.Solution.DieClass import DieClass

from CreateOrModifyTestData.HelperFunc.log_Message import logMessage
from Greedy_Optimized.GreedyInit import init_greedy_data
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Solution.remove_redundant_TDs import remove_redundant_TDs
from Greedy_Optimized.Solution.update_decision_variables import update_decision_variables
from Greedy_Optimized.Solution.update_values_after_touchdown import update_values_after_touchdown
from Greedy_Optimized.Touchdown.place_touchdown import place_touchdown
from Greedy_Optimized.Touchdown.select_next_touchdown import select_next_touchdown

# Given a Inputmap and Probecardsize and Previous TouchdownMap. Find the best n (loopcount) touchdowns, that would cover the highest touchdowns from 
# previous Maps
def find_best_tds_prev_maps(inputMapFilepath, probecardSize, prev_td_array, loop_count = 4, debugPrint = False):
    start_time = datetime.datetime.now()
    td_coord_list = []

    if(debugPrint):
        logMessage(f"Finding best Touchdowns to cover Prev Touchdown Maps | File: {inputMapFilepath.rsplit('/')[-1]} | PC: {probecardSize}")

    #Init/Load Data
    inputMap =  np.loadtxt(inputMapFilepath, dtype=int)
    probecard = getProbecardByName(probecardSize)
    waferMapObj = WaferMapClass(inputMap, probecard)
    previous_td_map = np.array(prev_td_array)

    if(debugPrint): print_two_arrays(previous_td_map, inputMap)
    least_flexible_map, least_flexible_map_strict = SolutionMapClass.create_least_flexible_maps("", waferMapObj)

    #The Main Array, with prebuild funcs
    dieMap: np.ndarray[DieClass] = np.empty(shape=waferMapObj.inputMap.shape, dtype=DieClass)
    #for x, y in np.ndindex(dieMap.shape):
    #    dieMap[x][y] = DieClass(x, y, inputMap_value = waferMapObj.inputMap[x][y],td_possible_as_site1=waferMapObj.possible_touchdowns_map[x][y])

    for x,y in waferMapObj.get_all_Mandatory_Touchdowns():
        #Write lesatFlex VAlues if coord is Mandatory TD
        dieMap[x][y] = DieClass(x, y, inputMap_value = waferMapObj.inputMap[x][y], td_possible_as_site1=waferMapObj.possible_touchdowns_map[x][y],
                                    least_flexible = least_flexible_map[x][y], least_flexible_strict = least_flexible_map_strict[x][y])
    #Fill in the rest dieMap, So no element is NONE. 
    for x,y in np.argwhere(dieMap == None):
        dieMap[x][y] = DieClass(x, y, inputMap_value = waferMapObj.inputMap[x][y], td_possible_as_site1=waferMapObj.possible_touchdowns_map[x][y])


    # The score_gain field from DieClass is repurposed to save the sum of prevTouchdownMap
    score_map = prev_map_update_score(dieMap, waferMapObj, previous_td_map)

    #Loop maximal loop_count times. But if all occurrences of the highest TOuchdown have been Touched, terminate aswell 
    for loopCount in range(loop_count): 
        if(check_all_highest_touched(dieMap, previous_td_map)):
            if(debugPrint): print(f"All highest TDs coverd - Found the first {loopCount} best Touchdowns: {td_coord_list}\n")
            return td_coord_list

        score_map = np.zeros(shape=dieMap.shape)
        for x, y in np.argwhere(dieMap != None):
            score_map[x][y] = dieMap[x][y].score_gain        

        #Select best Touchdown    
        maxRatingList = np.argwhere(score_map == np.max(score_map))
        td_x, td_y = maxRatingList[random.randint(0, len(maxRatingList) - 1)]
        td_coord_list.append((td_x, td_y))

        # Place selected Touchdown
        for die in get_values_by_mask(td_x, td_y, dieMap, waferMapObj.probecard.mask_1):
            die.touchdown += 1

        #Update Score
        prev_map_update_adjacent(td_x,td_y,waferMapObj,dieMap)
        prev_map_update_score(dieMap, waferMapObj, previous_td_map)


        #Print State after finishing 
        if(debugPrint): 
            print_touchdown_scores(dieMap)
            #print_Adjacent_(dieMap)

    
    if(debugPrint): print(f"Found the first {loop_count} best Touchdowns to cover Prev Touchdown Maps: {td_coord_list}\n")
    return td_coord_list

#Return True, if all occurrences of the highest TOuchdown have been Touched
def check_all_highest_touched(dieMap, previous_td_map):
    highest_prevTd = np.max(previous_td_map)
    highest_coordList = np.argwhere(previous_td_map == highest_prevTd)
    
    if(all(dieMap[x][y].touchdown >= 1 for x, y in highest_coordList)):
        return True

    return False

def print_touchdown_scores(dieMap):
    printMap_touchdown = np.zeros(shape=dieMap.shape, dtype=int)
    printMap_score = np.zeros(shape=dieMap.shape, dtype=int)   

    #for x, y in np.ndindex(self.dieMap.shape):
    for x, y in np.argwhere(dieMap != None):
        printMap_score[x][y] = dieMap[x][y].score_gain if dieMap[x][y].score_gain > -9999 else "0"
        printMap_touchdown[x][y] = dieMap[x][y].touchdown

    print_two_arrays(printMap_touchdown, printMap_score)

def print_Adjacent_(dieMap):
    printMap_adjacent = np.zeros(shape=dieMap.shape, dtype=int)

    #for x, y in np.ndindex(self.dieMap.shape):
    for x, y in np.argwhere(dieMap != None):
        printMap_adjacent[x][y] = dieMap[x][y].adjacent_flex_sum

    print_two_arrays(printMap_adjacent, printMap_adjacent)
