# Generate a Statistics file by Generating a Result for a Input map N (500) Times and repeating that M (5) Times.
# The Staistics File will contain all relevant Information like Min, Max, Mean, Median, Range, Variance, std_dev and all Values

import datetime
import os
import sys


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass
from Greedy_Optimized.Load_Safe.check_folder_exists import check_folder_exists
from Greedy_Optimized.Load_Safe.save_impossible_solution_json import save_impossible_solution_json
from Greedy_Optimized.Load_Safe.save_result_statistical_lists_json import save_result_statistical_lists_json
from Load_Safe.get_filepath_Json import get_filepath_Json
from HelperFunc.is_versionID_json_Impossible import is_versionID_json_Impossible
from HelperFunc.is_versionID_json_older import is_file_versionID_older
from HelperFunc.printTimestampDiff import printTimestampDiff
from GreedyMain import Greedy_Main

from inputMapsLibary import *
from probecardLibary import probecardDict_ForTesting

# Code Author: Peter Holland-Moritz
# Part of the article "Heuristic Approaches to the Wafer Covering Problem.", 2025
# compress the statistics from ALL relevant Runs down into a single file
if __name__ == "__main__":
    #removeOldMapsFromALLDir(filterFilepath)
    start_time = datetime.datetime.now()

    new_versionID = 5

    loopCount = 5
    solution_attempts = 500 #Multiprocessing attempts. Must be minimum 2 or else the list Operations fail


    # filepath_100Percent_Dict | filepath_Diagonal_Error_Dict | filepath_Mod4_Error_Dict
    Folder_MapTypes = {
        "Statistics_Greedy_100Percent": {"151x151":filepath_151x151_100Percent}, 
        "Statistics_Greedy_Mod4": {"151x151":filepath_151x151_Mod4_Error}, 
        "Statistics_Greedy_Diagonal": {"151x151":filepath_151x151_Diagonal_Error}, 
    }
    Folder_MapTypes = {
        "Data_Greedy_100Percent": filepath_100Percent_Dict, 
        "Data_Greedy_Mod4": filepath_Mod4_Error_Dict, 
        "Data_Greedy_Diagonal": filepath_Diagonal_Error_Dict, 
    }

    #ALL DIFFERENT NAMINGS FOR TUNING
    #NAME: 
    #   V_0X - IS TESTING
#[DONE] V_01 - Gewichtung 1: Only Score
#[DONE] V_02 - Gewichtung 2: Only adjacent_flex_sum (With same Rules to acceptable Touchdown as Score)
#[DONE] V_03 - Gewichtung 3: Only forbidden_distance_static
#[DONE] V_04 - Gewichtung 4: Score + optional_covered_buff_static

    ############  100% ÜBER-GEWICHTUNGEN DONE  ##############

#[DONE] V_05 - Gewichtung 5: Score + LeastFlex
#[DONE] V_06 - Gewichtung 6: Score + Dominanz
#[DONE] V_07 - Gewichtung 7: LeastFlex == Dominanz (Score + LeastFlex + Dominanz)
#[DONE] V_08 - Gewichtung 8: LeastFlex >> Dominanz (Score + LeastFlex + Dominanz) !!![SCHLECHTE LAUFZEIT]!!!
#[DONE] V_09 - Gewichtung 9: LeastFlex << Dominanz (Score + LeastFlex + Dominanz) (bestes)

    ############  FORCED OPTIONS DONE  ##############

    name_addition = "VXX_Statistics"
    print("START Generating: ", name_addition)
    curr_message="Saving total_time_ms of Run instead of Result Score"

    #Score, Adjacent, optional
    curr_weight = [20, 80, 0]
    weightSettingsObj = WeightSettingsClass(weight_score_gain=curr_weight[0], weight_adjacent_flex_sum=curr_weight[1], weight_forbidden_distance_and_optional_covered_static=curr_weight[2])
    print(f"[WEIGHT COMBINATION]: {name_addition} | Weights:{weightSettingsObj}")
    for folder_name, folder_filepaths in Folder_MapTypes.items():
        for waferMap_Size, inputMapFilepath in folder_filepaths.items():
            #save_folder = folder_name #Use for Manual overwrite
            save_folder = None

            for probecardName in probecardDict_ForTesting:
                #We allready well know which maps with Probeards are not solvavle -> SKip
                if (folder_name == "Statistics_Greedy_Diagonal" and (probecardName == "2x8" or probecardName == "2x16")) or (folder_name == "Statistics_Greedy_Mod4" and (probecardName == "2x8" or probecardName == "2x16" or probecardName == "4x4")) :
                    save_impossible_solution_json(get_filepath_Json(inputMapFilepath, probecardName, save_folder, name_addition), new_versionID, message="No Solution possible")
                    print(f"Skipped non Solvable Map: {folder_name} - {probecardName}")
                    continue

                local_start_time = datetime.datetime.now()
                filepath = get_filepath_Json(inputMapFilepath, probecardName, save_folder, name_addition)
                if(check_folder_exists(filepath) == False): raise Exception(f"The save folder '{os.path.dirname(filepath)}' does not exist.")

                #WE SKIP This Generation Step, if the Version ID of the Solution is atleast same to new_versionID
                if(is_file_versionID_older(filepath, new_versionID) or is_versionID_json_Impossible(filepath)):
                    continue

                #If version is Older, we generate File Anew and delete it to start off
                #removeSolutionFromDir(inputMapFilepath, probecard, save_folder)

                results_dict = {}
                for i in range(loopCount):
                    curr_resultList = Greedy_Main(inputMapFilepath, probecardName, save_folder=save_folder, versionID=new_versionID, parallelization=True, global_timeout_in_seconds = 7200, #1800 = 30 min | 7200 = 2h 
                                                    solution_attempts = solution_attempts, return_ALL_results= True, weightSettingsObj=weightSettingsObj)
                    
                    results_dict[i] = curr_resultList
                    if curr_resultList is None:
                        printTimestampDiff(local_start_time, f" [{i + 1}/{loopCount}] NO RESULT. Terminating/Skipping current LoopCount")
                        break

                    printTimestampDiff(local_start_time, f" [{i + 1}/{loopCount}] Staitstics Generated. Contains: {len(curr_resultList)} Elements")


                #If all results are None -> Save impossible Flag
                if all(value is None for value in results_dict.values()):
                    save_impossible_solution_json(get_filepath_Json(inputMapFilepath, probecardName, save_folder, name_addition), new_versionID, message="No Solution possible")
                    continue

                save_result_statistical_lists_json(results_dict, filepath, inputMapFilepath, probecardName, solution_attempts=solution_attempts, result_loops = loopCount,totalTime = (datetime.datetime.now() - local_start_time), versionID = new_versionID, message=curr_message)
                print("-----------")

            printTimestampDiff(start_time, f" - Total Time FOR FOLDER: {folder_name}")
        printTimestampDiff(start_time, " [FINISHED ALL] - Total Time FOR ALL FOLDERS")


