import numpy as np
from GlobalConstants import BASE_DATA_FILEPATH
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Touchdown.is_touchdown_possible import is_touchdown_possible

def save_Debug_Maps(solutionObj: SolutionMapClass):
    touchdown_map = np.zeros(shape=solutionObj.dieMap.shape, dtype=object)
    score_gain_map = np.zeros(shape=solutionObj.dieMap.shape, dtype=int) 
    adjacent_flex_sum_map = np.zeros(shape=solutionObj.dieMap.shape, dtype=int)

    #for x, y in np.ndindex(self.dieMap.shape):
    for x, y in np.argwhere(solutionObj.dieMap != None):
        touchdown_map[x][y] = round(solutionObj.dieMap[x][y].touchdown)
        if(solutionObj.dieMap[x][y].touchdown == 0 and solutionObj.dieMap[x][y].is_mandatory):
            touchdown_map[x][y] = "X"

        score_gain_map[x][y] = solutionObj.dieMap[x][y].score_gain
        adjacent_flex_sum_map[x][y] = solutionObj.dieMap[x][y].adjacent_flex_sum

    np.savetxt(BASE_DATA_FILEPATH + '/xDebug_Logs/touchdown_map.csv', touchdown_map, fmt='%s', delimiter=' ')
    np.savetxt(BASE_DATA_FILEPATH + '/xDebug_Logs/score_gain_map.csv', score_gain_map, fmt='%.1f', delimiter=' ')
    np.savetxt(BASE_DATA_FILEPATH + '/xDebug_Logs/adjacent_flex_sum_map.csv', adjacent_flex_sum_map, fmt='%.1f', delimiter=' ')
    np.savetxt(BASE_DATA_FILEPATH + '/xDebug_Logs/ratings_map.csv', solutionObj.ratings_map, fmt='%.1f', delimiter=' ')
    np.savetxt(BASE_DATA_FILEPATH + '/xDebug_Logs/forced_leastFlex_map.csv', solutionObj.forced_leastFlex_map, fmt='%.0f', delimiter=' ')
    np.savetxt(BASE_DATA_FILEPATH + '/xDebug_Logs/forced_dominante_map.csv', solutionObj.forced_dominante_map, fmt='%.0f', delimiter=' ')


def place_touchdown(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    #Check if selected TD is even possible. This is just a failsave to abort. Does not fix the issue or select a new one
    if(is_touchdown_possible(x, y, waferMapObj.inputMap, waferMapObj.probecard) == False):
        print(f"ILLEGAL TOUCHDOWN DETECTED at coords: {x} {y}.")
        #debug = get_values_by_mask(x, y, solutionObj.dieMap, waferMapObj.probecard.mask_1)
        save_Debug_Maps(solutionObj)

        return None, None
        #exit() #Stop the Programm. Is a return or Flag better than exit?
        

    #Get all Touchdown Dies and increment touchdownCount 
    for die in get_values_by_mask(x, y, solutionObj.dieMap, waferMapObj.probecard.mask_1):
        die.touchdown += 1

    #Mark the Site1 Touchdown and save it in the TD List
    solutionObj.dieMap[x][y].site1_touchdowns += 1
    solutionObj.td_Location_List.append((x,y))
