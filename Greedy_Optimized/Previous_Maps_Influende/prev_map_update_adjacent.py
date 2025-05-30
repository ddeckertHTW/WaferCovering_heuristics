from typing import List
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE, InputMapStatus_MANDATORY
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass


def prev_map_update_adjacent(x, y, waferMapObj: WaferMapClass, dieMap):
    die_list_mask_adjacent: List[DieClass] = get_values_by_mask(x,y, dieMap, waferMapObj.probecard.mask_adjacent)
    for die in die_list_mask_adjacent:
        #Abort, if TD would not be possible either way
        if not (die.td_possible_as_site1):
            continue

        td_Dies: List[DieClass] = get_values_by_mask(x,y, dieMap, waferMapObj.probecard.mask_1)
        #is_touchdown_creating_doubleTd
        if(any(die.touchdown != 0 and die.inputMap_value == InputMapStatus_MANDATORY for die in td_Dies)):
            dieMap[x][y].score_gain = IMPOSSIBLE_VALUE_NEGATIVE

            adjacent_Sum = get_values_by_mask(die.x, die.y, dieMap, waferMapObj.probecard.mask_1)
            die.adjacent_flex_sum = sum(die.least_flexible for die in adjacent_Sum)
        else:
            die.adjacent_flex_sum = IMPOSSIBLE_VALUE_POSITIVE