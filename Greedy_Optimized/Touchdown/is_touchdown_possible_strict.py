import numpy as np
from GlobalConstants import InputMapStatus_MANDATORY
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Probecard.ProbecardClass import ProbecardClass

# Returns True if touchdown on given x/y coords is possible. STRICT 
def is_touchdown_possible_strict(x, y, inputMap, probecard: ProbecardClass):
    values = get_values_by_mask(x, y, inputMap, probecard.mask_1)

    # All Values using the PC Maks must be NOT 0 and the len must be identically (at the border of the Array weird behavior)
    return np.all(values == InputMapStatus_MANDATORY) and len(values) == probecard.mask_1.len

#return is_touchdown_possible, is_touchdown_possible_strict in one function.
def is_touchdown_possible_and_strict(x, y, inputMap, probecard: ProbecardClass):
    values = get_values_by_mask(x, y, inputMap, probecard.mask_1)
    #len must be identically (at the border of the Array weird behavior)
    if len(values) != probecard.mask_1.len:
        return (False, False)

    # All Values using the PC Maks must be NOT 0 and the 
    return (np.all(values), np.all(values == InputMapStatus_MANDATORY))
