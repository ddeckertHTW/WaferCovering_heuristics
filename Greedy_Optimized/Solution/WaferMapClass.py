import numpy as np
from GlobalConstants import InputMapStatus_MANDATORY
from Greedy_Optimized.Probecard.ProbecardClass import ProbecardClass
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass
from Greedy_Optimized.Touchdown.create_possible_touchdowns_map import create_possible_touchdowns_maps

# The Object with fixed Values like inputMap/Probecard.
# Does not need deep Copy because no Values are changing
class WaferMapClass:
    def __init__(self, inputMap, probecard, td_scenario_list = None, weightSettingsObj:WeightSettingsClass = None):
        self.inputMap = inputMap
        self.probecard: ProbecardClass = probecard
        
        #The List that just dermines the first n Touchdowns 
        self.td_scenario_list = td_scenario_list
        
        # Value is True if the Bin in the input Map MUST be touched. Those are the Must Touch Dies
        self.mustTouchMap = np.zeros_like(inputMap, dtype=bool)
        self.mustTouchMap[inputMap == InputMapStatus_MANDATORY] = True #InputMapStatus.MANDATORY.value

        # Create Maps where cooridnate is TRUE if a touchdown CAN be Placed as Site 1. 
        self.possible_touchdowns_map, self.possible_touchdowns_map_strict = create_possible_touchdowns_maps(inputMap, probecard)

        #Just for the Tuning / Weighting of the decision Parameters. Can be ignored
        self.weightSettingsObj = weightSettingsObj

        #DEfault/Backup behavior in update_decision_variables
        if weightSettingsObj is None:
            print("!!! No Weights set for Decision Variables. Just using Zielfunktion Score")


    #TODO: Dopplung mit eintrag in DieClass. Nur ein was von beidem Machen. Performance??
    #Nameing is_touchdown_possible_by_coords OR is_touchdown_possible ??? Because we are checking BY coordinates
    def is_touchdown_possible_by_coords(self, x, y,):
        return self.possible_touchdowns_map[x, y]

    def is_touchdown_possible_by_coords_strict(self, x, y,):
        return self.possible_touchdowns_map_strict[x, y]

    def is_touchdown_mandatory_by_coords(self, x, y,):
        return self.mustTouchMap[x, y]

    #

    def get_all_Possible_Touchdowns(self):
        return np.argwhere(self.possible_touchdowns_map)
 
    def get_all_Possible_Touchdowns_strict(self):
        return np.argwhere(self.possible_touchdowns_map_strict)

    def get_all_Mandatory_Touchdowns(self):
        return np.argwhere(self.mustTouchMap)

    def get_all_Possible_Mandatory_Touchdowns(self):
        return np.argwhere((self.possible_touchdowns_map) & (self.mustTouchMap))

"""
    #Template
    def check_coordinate(self, i, j, x):
        return self.inputMap[i, j] == x

    def get_coordinates_with_value(self, x):
        return np.argwhere(self.inputMap == x)
    
    def find_coordinates(map1, map2, x, y):
        return np.argwhere((map1 == x) & (map2 == y))
"""