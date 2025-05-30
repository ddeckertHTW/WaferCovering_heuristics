import numpy as np
from GlobalConstants import InputMapStatus_FORBIDDEN
from Greedy_Optimized.Probecard import ProbecardClass
from Greedy_Optimized.Touchdown.is_touchdown_possible import is_touchdown_possible
from Greedy_Optimized.Touchdown.is_touchdown_possible_strict import is_touchdown_possible_and_strict, is_touchdown_possible_strict

# Represents if the touchdown in this coordinate AS SITE 1 would be possible. Not if the die can be covered at all
# Return Map where every 1 represents a possible Touchdown. 0 If not possible
def create_possible_touchdowns_maps(inputMap, probecard: ProbecardClass):
    possible_touchdowns = np.zeros_like(inputMap, dtype=bool)
    possible_touchdowns_strict = np.zeros_like(inputMap, dtype=bool)

    # Go over all coords, that are not Forbidden. And check if touchdown shape would be allowed
    for x, y in np.argwhere(inputMap != InputMapStatus_FORBIDDEN): #InputMapStatus.FORBIDDEN.value
        possible_touchdowns[x][y], possible_touchdowns_strict[x][y] = is_touchdown_possible_and_strict(x, y, inputMap, probecard)
        """possible_touchdowns[x][y] = is_touchdown_possible(x, y, inputMap, probecard)
        
        #We can use the previously calculated create_possible_touchdowns_map and only check those elements. As strict is a subset of it
        if(possible_touchdowns[x][y]):
            possible_touchdowns_strict[x][y] = is_touchdown_possible_strict(x, y, inputMap, probecard)
        """
    return possible_touchdowns, possible_touchdowns_strict
