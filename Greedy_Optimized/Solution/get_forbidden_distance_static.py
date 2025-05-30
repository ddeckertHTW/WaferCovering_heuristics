from typing import List

import numpy as np
from GlobalConstants import InputMapStatus_FORBIDDEN, InputMapStatus_OPTIONAL
from Greedy_Optimized.Probecard import ProbecardClass
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

# Add a Buff regarding to distance to the nearest Forbiden Die. Touchdowns near Forbidden Dies have a lot less possible Options
# So by rewarding these Touchdowns with fewer Options they get placed early and dont cause unneeded double Touchdowns
# The Lower the distance -> The Bigger the Reward

def get_forbidden_distance_static(td_dies: List[DieClass], waferMapObj: WaferMapClass):
    # Get the distance of all touchded Dies to the nearest forbidden Die.
    # By taking the Sum of all Dies / SiteCount -> We get the average Distance of the whole Touchdown
    distance_sum = 0
    for die in td_dies:
        distance_sum += find_nearest_distance_to_forbidden_Die((die.x, die.y), waferMapObj.inputMap)

    average_distance = distance_sum / waferMapObj.probecard.sitesCount
    return average_distance


# FInd the distance of the given coordinate to the nearest forbidden Die.
def find_nearest_distance_to_forbidden_Die(coord, inputMap, search_value=InputMapStatus_FORBIDDEN):
    # Get the coordinates of all cells with the value 'target_value'
    target_coords = np.argwhere(inputMap == search_value)
    
    if target_coords.size == 0:
        return None  # No target value in the array
    
    # Compute the Euclidean distance from the input coordinate to each target cell
    distances = np.linalg.norm(target_coords - np.array(coord), axis=1)
    
    # Return the minimum distance
    return np.min(distances)
