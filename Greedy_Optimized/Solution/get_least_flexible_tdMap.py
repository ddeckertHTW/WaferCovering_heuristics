from typing import List

import numpy as np
from GlobalConstants import InputMapStatus_OPTIONAL
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

# Instead of looking at each individual Die and calculating the placement Options (Needs ProbecardSize Mask Operations)
# Loop over shape4 Dies. Track in a new Array how many TDs were possible. We only need Shape3 in the Update Process, but have to calculate for all Dies in shape3. So one Minkowski SUm FURTHER -> mask4
def get_least_flexible_tdMap(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    leastFlexMap = np.zeros_like(waferMapObj.inputMap)

    #for curr_x, curr_y in waferMapObj.get_all_Possible_Touchdowns():
        #die = solutionObj.dieMap[curr_x][curr_y]
    die_list_mask4: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_4)
    for die in die_list_mask4:
        #If TD cannot even be placed -> continue and leave leastFlex Value as zero (initialized)
        if die.td_possible_as_site1 == False:
            continue

        #For every die, check if there are not allready touchdowns. If none -> Add to all curr_dies Coordinates +1 Option
        curr_die_List = get_values_by_mask(die.x, die.y, solutionObj.dieMap, waferMapObj.probecard.mask_1)


        # All Dies of this hypothetical Touchdown must be 0 if mandatory. Optional does not matter. Forbidden dont allow
        #is_mandatory_or_optional ODER die.inputMap_value == InputMapStatus_OPTIONAL
        if all((die.touchdown == 0 and die.is_mandatory) or die.inputMap_value == InputMapStatus_OPTIONAL for die in curr_die_List):
            #No Touchdown allready placed -> Increase the count on the Checked dies. 
            for die in curr_die_List:
                leastFlexMap[die.x][die.y] += 1

    return leastFlexMap

"""
def get_least_flexible_tdMap_and_strict(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    leastFlexMap = np.zeros_like(waferMapObj.inputMap)
    leastFlexMap_strict = np.zeros_like(waferMapObj.inputMap)

    die_list_mask4: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_4)
    for checking_die in die_list_mask4:
        #For every die, check if there are not allready touchdowns. If none -> Add to all curr_dies Coordinates +1 Option
        curr_die_List = get_values_by_mask(checking_die.x, checking_die.y, solutionObj.dieMap, waferMapObj.probecard.mask_1)

        if all(die.touchdown == 0 and die.is_mandatory_or_optional for die in curr_die_List):
            #No Touchdown allready placed -> Increase the count on the Checked dies. 
            for die in curr_die_List:
                leastFlexMap[die.x][die.y] += 1

        #For Strict Map - Check if ALL Bins are Mandatory                
        if all(die.touchdown == 0 and die.die_mandatory_and_touchable for die in curr_die_List):
            for die in curr_die_List:
                leastFlexMap_strict[die.x][die.y] += 1

    return leastFlexMap, leastFlexMap_strict
"""