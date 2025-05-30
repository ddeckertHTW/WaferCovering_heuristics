from GlobalConstants import InputMapStatus_MANDATORY
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

#Returns True, if any die has touchdown Value >= 1. False, if all dies have 0 Touchdowns. (Only look at Mandatory TDs)
def is_touchdown_creating_doubleTd(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    die_List = get_values_by_mask(x, y, solutionObj.dieMap, waferMapObj.probecard.mask_1)

    return any(die.touchdown != 0 and die.inputMap_value == InputMapStatus_MANDATORY for die in die_List)