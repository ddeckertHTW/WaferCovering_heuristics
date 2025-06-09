# Generate a Solution to a Inputfile and then STACK another Result on TOP. This generats the Stacked Maps that try to avoid 
# to re-use old Stacked points

import datetime
import os
import sys

import numpy as np

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from Greedy_Optimized.Load_Safe.check_folder_exists import check_folder_exists
from inputMapsLibary import *
from Greedy_Optimized.Load_Safe.save_td_map_chain_json import save_td_map_chain_json
from Greedy_Optimized.Previous_Maps_Influende.find_best_tds_prev_maps import find_best_tds_prev_maps
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass

from Greedy_Optimized.Load_Safe.load_json_data import load_json_data
from Load_Safe.removeSolutionFromDir import removeSolutionFromDir
from Load_Safe.get_filepath_Json import get_filepath_Json
from HelperFunc.is_versionID_json_Impossible import is_versionID_json_Impossible
from HelperFunc.is_versionID_json_older import is_file_versionID_older
from HelperFunc.printTimestampDiff import printTimestampDiff
from GreedyMain import Greedy_Main

from inputMapsLibary import filepath_100Percent_Dict, filepath_Diagonal_Error_Dict, filepath_Mod4_Error_Dict
from probecardLibary import probecardDict_ForTesting

scriptFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#IMPORTANT FOR DELETING ONLY OLD FILES. AND NOT NEW ONES. If Version in json Solution is lower -> delete file to regenerate
new_versionID = None

# Code Author: Peter Holland-Moritz
# Part of the article "Heuristic Approaches to the Wafer Covering Problem.", 2025
# Re-Generates all COmbinations of Probecard x InputMap and saves them in the DataFolderPath
if __name__ == "__main__":
    #removeOldMapsFromALLDir(filterFilepath)
    startTime = datetime.datetime.now()

    # filepath_100Percent_Dict | filepath_Diagonal_Error_Dict | filepath_Mod4_Error_Dict
    Folder_MapTypes = {
        "Data_Greedy_100Percent": [filepath_15x15_100Percent], 
        #"Data_Greedy_100Percent": filepath_100Percent_Dict, 
        #"Data_Greedy_100Percent": [filepath_51x51_100Percent, filepath_101x101_100Percent], 
        #"Data_Greedy_Mod4": filepath_Mod4_Error_Dict, 
        #"Data_Greedy_Diagonal": filepath_Diagonal_Error_Dict, 
    }


    curr_pre_td_count = 1
    maps_generate_count = 10
    greedy_loop_count = 250

    curr_weight = [20, 80, 0]
    weightSettingsObj = WeightSettingsClass(weight_score_gain=curr_weight[0], weight_adjacent_flex_sum=curr_weight[1], weight_forbidden_distance_and_optional_covered_static=curr_weight[2])

    #First Map is allready generated, so calc one less 
    maps_generate_count = maps_generate_count - 1
    for folder_name, folder_filepath_dict in Folder_MapTypes.items():
        #save_folder = folder_name #Use for Manual overwrite
        save_folder = None

        for inputMapFilepath in folder_filepath_dict:
            for probecard in probecardDict_ForTesting:

                local_start_time = datetime.datetime.now()
                filepath = get_filepath_Json(inputMapFilepath, probecard, save_folder, name_addition="TD_CHAIN")

                if(check_folder_exists(filepath) == False): raise Exception(f"The save folder '{os.path.dirname(filepath)}' does not exist.")

                #WE SKIP This Generation Step, if the Version ID of the Solution is atleast same to new_versionID
                if(is_file_versionID_older(filepath, new_versionID) or is_versionID_json_Impossible(filepath)):
                    continue

                # USE THIS TO LOAD IN THE BEST RESULT FROM ALREADY SAVED FILE
                #json_data = load_json_data("...")
                #if json_data is None or 'tdMap' not in json_data:
                #    continue

                #prev_td_map = np.array(json_data['tdMap'])
                #Init the prev_td_map with best result from JSON
                #sum_td_maps = prev_td_map
                sum_td_maps = None

                tdMap_List = []
                tdMap_Sum_List = []
                #The first Map is from the Json
                #tdMap_List.append(prev_td_map)
                #tdMap_Sum_List.append(prev_td_map)

                for i in range(0,maps_generate_count):
                    if sum_td_maps is not None:
                        best_tds_for_prev_maps = find_best_tds_prev_maps(inputMapFilepath, probecard, prev_td_array = sum_td_maps, debugPrint=False, loop_count = curr_pre_td_count)
                        printTimestampDiff(local_start_time, f" - [{i}/{maps_generate_count}] - Found {best_tds_for_prev_maps.__len__()}/{curr_pre_td_count} best Touchdowns, to cover previous TdMaps: {best_tds_for_prev_maps}")
                    else: 
                        best_tds_for_prev_maps = None
                    
                    #Generate a new "best Result Map" to use as input for next best touchdowns prevMaps
                    curr_td_map = Greedy_Main(inputMapFilepath, probecard, td_scenario_list=best_tds_for_prev_maps, saveResults=False, debugPrint=False,
                                               solution_attempts=greedy_loop_count, parallelization=True, versionID = new_versionID, global_timeout_in_seconds=7200, weightSettingsObj=weightSettingsObj)

                    if sum_td_maps is None: sum_td_maps = curr_td_map
                    else: 
                        sum_td_maps = curr_td_map + sum_td_maps
                    
                    #Save Maps
                    tdMap_List.append(curr_td_map)
                    tdMap_Sum_List.append(sum_td_maps)

                save_td_map_chain_json(tdMap_List, tdMap_Sum_List, filepath, new_versionID)


                exit()
                
            printTimestampDiff(local_start_time, f" [SUCCESS] Generated {maps_generate_count} Stacked Maps. Saving all to file: {filepath}")
        printTimestampDiff(startTime, f" - Total Time FOR FOLDER: {folder_name}")
    printTimestampDiff(startTime, " - Total Time FOR ALL FOLDERS")


