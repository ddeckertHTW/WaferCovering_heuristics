import datetime
import os
import sys


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass

from Greedy_Optimized.HelperFunc.get_distinct_weight_pairs import get_distinct_weight_pairs
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


    #ALL DIFFERENT NAMINGS FOR TUNING
    #NAME: 
    #   V_0X - IS TESTING
#[DONE] V_01 - Gewichtung 1: Only Score
#[DONE] V_02 - Gewichtung 2: Only adjacent_flex_sum (With same Rules to acceptable Touchdown as Score)
    #   V_03 - Gewichtung 3: Only forbidden_distance_static
    #   V_04 - Gewichtung 4: Score + optional_covered_buff_static

    ############  100% ÜBER-GEWICHTUNGEN DONE  ##############

#[DONE] V_05 - Gewichtung 5: Score + LeastFlex
#[DONE] V_06 - Gewichtung 6: Score + Dominanz
#[DONE] V_07 - Gewichtung 7: LeastFlex == Dominanz (Score + LeastFlex + Dominanz)
#[DONE] V_08 - Gewichtung 8: LeastFlex >> Dominanz (Score + LeastFlex + Dominanz) !!![SCHLECHTE LAUFZEIT]!!!
#[DONE] V_09 - Gewichtung 9: LeastFlex << Dominanz (Score + LeastFlex + Dominanz) (bestes)

    ############  FORCED OPTIONS DONE  ##############


#First Parameters With weights for Score + Adjacent
"""weights_dict = {
    10: (100, 0),
    11: (95, 5),
    12: (90, 10),
    13: (85, 15),
    14: (80, 20),
    15: (75, 25),
    16: (70, 30),
    17: (65, 35),
    18: (60, 40),
    19: (55, 45),
    20: (50, 50),
    21: (45, 55),
    22: (40, 60),
    23: (35, 65),
    24: (30, 70), #Erster Eindruck sagt, das ist ganz gut bei 2x8
    25: (25, 75),
    26: (20, 80),
    27: (15, 85),
    28: (10, 90),
    29: (5, 95),
    30: (0, 100)
}"""

weights_dict = {
    34: (0, 0, 100),
    35: (0, 10, 90),
    36: (0, 20, 80),
    37: (0, 30, 70),
    38: (0, 40, 60),
    39: (0, 50, 50),
    40: (0, 60, 40),
    41: (0, 70, 30),
    42: (0, 80, 20),
    43: (0, 90, 10),
    44: (0, 100, 0),
    45: (10, 0, 90),
    46: (10, 10, 80),
    47: (10, 20, 70),
    48: (10, 30, 60),
    49: (10, 40, 50),
    50: (10, 50, 40),
    51: (10, 60, 30),
    52: (10, 70, 20),
    53: (10, 80, 10),
    54: (10, 90, 0),
    55: (20, 0, 80),
    56: (20, 10, 70),
    57: (20, 20, 60),
    58: (20, 30, 50),
    59: (20, 40, 40),
    60: (20, 50, 30),
    61: (20, 60, 20),
    62: (20, 70, 10),
    63: (20, 80, 0),
    64: (30, 0, 70),
    65: (30, 10, 60),
    66: (30, 20, 50),
    67: (30, 30, 40),
    68: (30, 40, 30),
    69: (30, 50, 20),
    70: (30, 60, 10),
    71: (30, 70, 0),
    72: (40, 0, 60),
    73: (40, 10, 50),
    74: (40, 20, 40),
    75: (40, 30, 30),
    76: (40, 40, 20),
    77: (40, 50, 10),
    78: (40, 60, 0),
    79: (50, 0, 50),
    80: (50, 10, 40),
    81: (50, 20, 30),
    82: (50, 30, 20),
    83: (50, 40, 10),
    84: (50, 50, 0),
    85: (60, 0, 40),
    86: (60, 10, 30),
    87: (60, 20, 20),
    88: (60, 30, 10),
    89: (60, 40, 0),
    90: (70, 0, 30),
    91: (70, 10, 20),
    92: (70, 20, 10),
    93: (70, 30, 0),
    94: (80, 0, 20),
    95: (80, 10, 10),
    96: (80, 20, 0),
    97: (90, 0, 10),
    98: (90, 10, 0),
    99: (100, 0, 0),
}

# compress the statistics from ALL relevant Runs down into a single file
if __name__ == "__main__":
    start_time = datetime.datetime.now()

    new_versionID = 1

    loopCount = 5
    solution_attempts = 500 #Multiprocessing attempts. Must be minimum 2 or else the list Operations fail

    # filepath_100Percent_Dict | filepath_Diagonal_Error_Dict | filepath_Mod4_Error_Dict
    Folder_MapTypes = {
        "Statistics_Greedy_100Percent": filepath_151x151_100Percent, 
        "Statistics_Greedy_Mod4": filepath_151x151_Mod4_Error, 
        "Statistics_Greedy_Diagonal": filepath_151x151_Diagonal_Error, 
    }

    for version_ID, curr_weight in weights_dict.items():
        name_addition = f"V{version_ID}_Statistics"
        #The Object, that is passed into waferMapObj to set the weights in the decision Function
        #weightSettingsObj = WeightSettingsClass(weight_score_gain=curr_weight[0], weight_adjacent_flex_sum=curr_weight[1], weight_forbidden_distance_and_optional_covered_static=0)
        weightSettingsObj = WeightSettingsClass(weight_score_gain=curr_weight[0], weight_adjacent_flex_sum=curr_weight[1], weight_forbidden_distance_and_optional_covered_static=curr_weight[2])

        print("-----------")
        print(f"[START NEW WEIGHT COMBINATION]: {name_addition} | Weights:{weightSettingsObj}")
        print("-----------")
        
        for folder_name, inputMapFilepath in Folder_MapTypes.items():
            save_folder = folder_name

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

                #Extra field that saves what the tuning weight was (Message)
                save_result_statistical_lists_json(results_dict, filepath, inputMapFilepath, probecardName, solution_attempts=solution_attempts, result_loops = loopCount,totalTime = (datetime.datetime.now() - local_start_time), versionID = new_versionID, message=str(weightSettingsObj))
                print("-----------")

            printTimestampDiff(start_time, f" - Total Time FOR FOLDER: {folder_name}")
        printTimestampDiff(start_time, " [FINISHED CURRENT WEIGHT] - Total Time FOR ALL FOLDERS")
    printTimestampDiff(start_time, " [FINISHED ALL WEIGHTS] - Total Time FOR ALL WEIGHTS")


