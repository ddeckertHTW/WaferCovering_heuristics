import datetime
import time
import numpy as np
from GlobalConstants import PENALTY_SCORE, InputMapStatus_MANDATORY
from Greedy_Optimized.HelperFunc.convert_TimestampDiff_to_string import convert_TimestampDiff_to_string
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.get_result_score import get_result_score

# The Result Solution which GreedyLoop is generating
class ResultClass:
    def __init__(self, solutionObj: SolutionMapClass, inputMap, init_time_total: datetime.timedelta, loop_start_time: datetime.datetime, redundant_Tds = 0):
        #Convert touchdown Attribut of solutionObj.dieMap to a seperate 2D np array 
        touchdown_map, touchdown_location_map = self.create_td_maps(solutionObj)
        self.touchdown_map = touchdown_map
        self.touchdown_location_map = touchdown_location_map #Site 1 Location

        #Just the List in what Order the Touchdowns were placed. Save only Site1 coords 
        self.td_Location_List = solutionObj.td_Location_List.copy()

        # The dictionary with Touchdown Count {1: 224, 2: 32} 
        self.Rating_All = self.get_TD_count_dict(self.touchdown_map)
        self.Rating_Mandatory = self.get_TD_count_dict_mandatory(self.touchdown_map, inputMap)
        self.Rating_Mandatory_Percentages = self.get_TD_count_percentages_mandatory(self.Rating_Mandatory)

        # The Score / Value of the Zielfunktion which detemines how good the Solution is. The lower the better...
        self.final_score = get_result_score(self.Rating_Mandatory)
        self.final_score_All = get_result_score(self.Rating_All)

        # The Count of How many Touchdowns were placed. Like: 15
        self.td_Count = solutionObj.td_Location_List.__len__()
        
        # The Sum of just the Touchdown Map. So Value like 288
        self.td_sum_All = self.get_td_sum(self.touchdown_map)
        self.td_sum_Mandatory = self.get_td_sum_mandatory(self.touchdown_map, inputMap)

        #Just a counter, how many redundant Touchdowns were removed in this Solution, (For debug. Can be deleted)
        self.redundant_Tds = redundant_Tds
        
        # Time taken for each secion 
        self.init_time_ms = init_time_total
        self.loop_time_ms = datetime.datetime.now() - loop_start_time
        self.total_time_ms = self.init_time_ms + self.loop_time_ms  #GETS USED FOR SAVING THE FILE

        self.init_time_string = convert_TimestampDiff_to_string(self.init_time_ms)
        self.loop_time_string = convert_TimestampDiff_to_string(self.loop_time_ms)
        self.total_time_string = convert_TimestampDiff_to_string(self.total_time_ms)

    
    def create_td_maps(self, solutionObj: SolutionMapClass):
        touchdown_map = np.zeros(shape=solutionObj.dieMap.shape, dtype=int)
        touchdown_location_map = np.zeros(shape=solutionObj.dieMap.shape, dtype=int) #Site 1 Location

        #for x, y in np.ndindex(self.dieMap.shape):
        for x, y in np.argwhere(solutionObj.dieMap != None):
            touchdown_map[x][y] = solutionObj.dieMap[x][y].touchdown
            touchdown_location_map[x][y] = solutionObj.dieMap[x][y].site1_touchdowns

        return touchdown_map, touchdown_location_map

    #Get the dictionary  {1: 224, 2: 32} 
    def get_TD_count_dict(self, touchdown_map):
        filtered_values = touchdown_map[np.where(touchdown_map != 0)]
        unique_values, counts = np.unique(filtered_values, return_counts=True)
        return dict(zip(unique_values, counts))
    
    def get_TD_count_dict_mandatory(self, touchdown_map, inputMap):
        filtered_values = touchdown_map[np.where(touchdown_map != 0) and np.where(inputMap == InputMapStatus_MANDATORY)]
        unique_values, counts = np.unique(filtered_values, return_counts=True)
        return dict(zip(unique_values, counts))
    
    #Calc the Percentage of each Unique TD Count (1: 95%, 2: 5%)
    def get_TD_count_percentages_mandatory(self, count_mandatory_dict):
        total_sum = sum(count_mandatory_dict.values())
        percentage_dict = {key: round((value / total_sum) * 100, 2) for key, value in count_mandatory_dict.items()}
        return percentage_dict

    def get_td_sum(self, touchdown_map):
        return np.sum(touchdown_map)
    
    def get_td_sum_mandatory(self, touchdown_map, inputMap):
        filteredMap = touchdown_map[np.where(inputMap == InputMapStatus_MANDATORY)]
        return np.sum(filteredMap)