from typing import List
import numpy as np
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE, InputMapStatus_FORBIDDEN, InputMapStatus_MANDATORY, InputMapStatus_OPTIONAL
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

def prev_map_update_score(dieMap: np.ndarray[DieClass], waferMapObj: WaferMapClass, previous_td_map):
    #For every die where Touchdown would be possible. Update value
    for x, y in np.ndindex(dieMap.shape):
        td_Dies = None
        if (dieMap[x][y].td_possible_as_site1 == 1):
            #get Touchdown Shape dies and add all the Previous Touchdown count together
            td_Dies: List[DieClass] = get_values_by_mask(x,y, dieMap, waferMapObj.probecard.mask_1)

            #Check if Touchdown would create a double TD
            if(any(die.touchdown != 0 and die.inputMap_value == InputMapStatus_MANDATORY for die in td_Dies)):
                #print("Is Creating double", x, y)
                dieMap[x][y].score_gain = IMPOSSIBLE_VALUE_NEGATIVE
                dieMap[x][y].adjacent_flex_sum = IMPOSSIBLE_VALUE_POSITIVE
                continue

            currRating = 0
            for die in td_Dies:
                # Case 1: Should not be possible...
                if(die.inputMap_value == InputMapStatus_FORBIDDEN):
                    dieMap[x][y].score_gain = IMPOSSIBLE_VALUE_NEGATIVE
                    break
                
                #Case 2: Optional -> Rating does not amtter
                if(die.inputMap_value == InputMapStatus_OPTIONAL): 
                    currRating += -0.1
                
                #Case 3: Must TOuch Die -> Rate based on the PrevTD Value. Linear
                if(die.inputMap_value == InputMapStatus_MANDATORY): 
                    currRating += previous_td_map[x][y]
            
            dieMap[x][y].score_gain = currRating + (dieMap[x][y].adjacent_flex_sum / waferMapObj.probecard.maxSitesSum)
            #print("Added Adjacent Buff: ", (dieMap[x][y].adjacent_flex_sum / waferMapObj.probecard.sitesCount))


       