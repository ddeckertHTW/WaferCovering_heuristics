import numpy as np
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Probecard.ProbecardClass import ProbecardClass

# Returns True if touchdown on given x/y coords is possible. 
def is_touchdown_possible(x, y, inputMap, probecard: ProbecardClass):
    values = get_values_by_mask(x, y, inputMap, probecard.mask_1)

    # All Values using the PC Maks must be NOT 0 and the len must be identically (at the border of the Array weird behavior)
    return np.all(values) and len(values) == probecard.mask_1.len

    #return np.all(values != InputMapStatus.FORBIDDEN) and len(values) == probecard.mask_1.len
    # # np.all(values) returns True if NO 0 is within the values. May be faster than "clear Readability"