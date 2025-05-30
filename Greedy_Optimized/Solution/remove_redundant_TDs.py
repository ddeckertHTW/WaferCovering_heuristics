from typing import List
import numpy as np
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

#With hard problems, there are Situations, wehere a complete redundant touchdown was placed, that can be removed.
# Touchdown must be 2 or higher for every DIE of probecard shape
def remove_redundant_TDs(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, debugPrint = False):
    original_list_len = solutionObj.td_Location_List.__len__()

    for x, y in np.ndindex(solutionObj.dieMap.shape):
        if(solutionObj.dieMap[x][y].touchdown >= 2):
            die_List: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_1)
            #If touchdown Counter of this shape is all above 2. Then we might be able to remove this redundant touchdown
            if all(die.touchdown >= 2 for die in die_List):
                #We can only remove the Touchdown, if it was set as SITE 1. Otherwise removing is not possible... as the double shape comes from other touchdowns
                if (x,y) in solutionObj.td_Location_List:
                    solutionObj.td_Location_List.remove((x, y))

                    #Remove Touchdown -> -1 on counter
                    for curr_die in die_List:
                        curr_die.touchdown = curr_die.touchdown - 1

    if(debugPrint and original_list_len - solutionObj.td_Location_List.__len__() >= 1):    
        print(f"Redundant Touchdowns found: {original_list_len - solutionObj.td_Location_List.__len__()}. Removing from Solution")

    #Return count on how many elements were removed, to save in File
    return original_list_len - solutionObj.td_Location_List.__len__()