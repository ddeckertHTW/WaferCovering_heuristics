# Get the first Touchdown Location to cover the given bin (coordintaes) WITHOUT creating a double Touchdown. 
# USE when only one LeastFlexible Option exist -> gets this one Option
# ONLY POSSIBLE WHEN Coordinate has LeastFlexible == 1
    
from GlobalConstants import InputMapStatus_OPTIONAL
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Probecard.get_offset_toSite1 import get_offset_toSite1
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Touchdown.is_touchdown_possible import is_touchdown_possible


def get_only_least_flex_option(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass): 
    # Go through all Probecard Sites and test them for beeing the new Site 1 
    for coord in waferMapObj.probecard.binDict.values():
        die_list = get_values_by_mask(x - coord[0], y - coord[1], solutionObj.dieMap, waferMapObj.probecard.mask_1)

#       if all(die.touchdown == 0 for die in die_list):
        if all((die.touchdown == 0 and die.is_mandatory) or die.inputMap_value == InputMapStatus_OPTIONAL for die in die_list):
            coordOffset = get_offset_toSite1(waferMapObj.probecard.binDict, coord[0], coord[1])
            if(is_touchdown_possible(x + coordOffset[0], y + coordOffset[1], waferMapObj.inputMap, waferMapObj.probecard) == False):
                continue

            return (x + coordOffset[0], y + coordOffset[1])

    raise Exception("ERROR. COULD NOT FIND THE ONLY POSSIBLE PLACEMENT OPTION!!!")