#region All Imports
import datetime
import numpy as np

import sys; import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Greedy_Optimized.Load_Safe.get_filepath_Json import get_filepath_Json
from Greedy_Optimized.Load_Safe.load_json_data import load_json_data
from Greedy_Optimized.Previous_Maps_Influende.find_best_tds_prev_maps import find_best_tds_prev_maps
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass

from Greedy_Optimized.Load_Safe.save_impossible_solution_json import save_impossible_solution_json
from Greedy_Optimized.Load_Safe.save_result_json import save_result_json
from Greedy_Optimized.GreedyInit import init_greedy_data
from Greedy_Optimized.GreedyLoop import Greedy_Loop
from Greedy_Optimized.HelperFunc.printTimestampDiff import printTimestampDiff
from CreateOrModifyTestData.HelperFunc.log_Message import logMessage
from Greedy_Optimized.Parallelization.Multiprocessing_Greedy import get_max_simultaneous_processes, multiprocessing_greedy

from inputMapsLibary import *
from probecardLibary import probecardDict_ForTesting

#endregion All Imports

#Base Folder to save in
SAVE_FOLDER = "Data_Greedy"

#For Testing - in which touchdown which pre determined Touchdown is placed
#td_scenario_list = {0: (4,4), 1:(5,5), 2:(6,6)}
#td_scenario_list = None

#LOADING EXISTING TOUCHDOWNS !!!???? 
def Greedy_Main(inputMapFilepath, probecardSize, saveResults=False, debugPrint=False, td_scenario_list = None,
                solution_attempts = 1, parallelization = False, global_timeout_in_seconds = 1800, max_simultaneous_processes = None, 
                versionID = 0, save_folder = SAVE_FOLDER, return_ALL_results = False, weightSettingsObj:WeightSettingsClass = None):
    start_time = datetime.datetime.now()

    logMessage(f"Start Main | File: {inputMapFilepath.rsplit('/')[-1]} | PC: {probecardSize} | Saving: {saveResults} | ID: {versionID} | Timeout: {global_timeout_in_seconds}")

    #Load Data and init Classes
    waferMapObj, solutionObj = init_greedy_data(inputMapFilepath, probecardSize, td_scenario_list, weightSettingsObj)
    init_timeDiff = datetime.datetime.now() - start_time 

    #Check if there are any Dies that have 0 leastFlex OPTIONS but are mandatory Touchdowns
    if solutionObj.isSoluitionImpossible():
        #If statisitc collecting all results. Discard any fail
        if(return_ALL_results): return None

        print(f"[NOT SOLVABLE] - TERMINATING RUN | File: {inputMapFilepath.rsplit('/')[-1]} | PC: {probecardSize}")
        #If saveResult is true -> Save the Impossible to Solve Flag in Json File: {"versionID": "IMPOSSIBLE"}
        save_impossible_solution_json(get_filepath_Json(inputMapFilepath, probecardSize, save_folder), versionID)
        #Extra Linebreak or some Symbol to show we are DONE
        print()
        return

    if debugPrint: # DEBUG PRINT
        printTimestampDiff(start_time, f" - Time for Loading and init Data")

    # Normal Try
    if(solution_attempts == 1 or parallelization == False):
        resultObj = Greedy_Loop(waferMapObj, solutionObj, debugPrint=debugPrint, init_time_total=init_timeDiff)
        finished_attempts = 1 #Just so we dont break save Function. THis parameter is needed

    # parallelization where Multiple resultObj were generated and only the best one is returned
    elif (parallelization):
        if(debugPrint): printTimestampDiff(start_time, f" - Start Multiprocessing | attempts: {solution_attempts} | max_workers: {get_max_simultaneous_processes(max_simultaneous_processes)} | timeout: {global_timeout_in_seconds} sec")
        #print(f"Multiprocessing: attempts: {solution_attempts} | max_workers: {get_max_simultaneous_processes(max_simultaneous_processes)} | timeout: {global_timeout_in_seconds} sec")
        resultObj, finished_attempts = multiprocessing_greedy(waferMapObj, solutionObj, attempt_count=solution_attempts, init_time_total = init_timeDiff,
                                         global_timeout_in_seconds=global_timeout_in_seconds, max_simultaneous_processes=max_simultaneous_processes,
                                         return_ALL_results = return_ALL_results )
    
    #TODO: In Multiprocessing - SAVE Mathematically Average / Mean for all Runs??? Only best Run (time) is not really enaugh...

    #If Error / Termination occured in GreedyLoop -> resultObj is None. Abort here to avoid errorhandling
    if resultObj is None:
        return
    #When the List of all results is needed (from Multiprocessing)
    if return_ALL_results:
        return resultObj

    #Best Solution Data - Print
    printTimestampDiff(start_time, f" - Total Time | Result Time: {resultObj.total_time_string} " + 
                    f" | Score: {resultObj.final_score} | Rating: {resultObj.Rating_Mandatory} | Percentage: {resultObj.Rating_Mandatory_Percentages} | td Count: {resultObj.td_Count}")

    # SAVE TO JSON
    if (saveResults):
        save_result_json(resultObj, inputMap_filepath = inputMapFilepath, pcSize = probecardSize, totalTime = (datetime.datetime.now() - start_time), solution_attempts = solution_attempts, finished_attempts = finished_attempts, 
                         saveFilePath = get_filepath_Json(inputMapFilepath, probecardSize, save_folder), versionID = versionID)
    
    #Extra Linebreak or some Symbol to show we are DONE
    print()

    return resultObj.touchdown_map


#VERSIONING TO AVOID OVERWRITING GOOD SOLUTIONS. README File has versioning ID Info
#IF set to None -> Will allways overwrite
curr_versionID = 0 #Keep at 0 to not overwrite while testing... 

# SET THE VALUES FOR MANUAL DEBUGGING
currInputMapFilepath = filepath_15x15_100Percent
#currInputMapFilepath = filepath_151x151_100Percent
#currInputMapFilepath = filepath_101x101_100Percent
#currInputMapFilepath = filepath_101x101_Diagonal_Error
#currInputMapFilepath = filepath_101x101_Mod4_Error

currProbecardSIze = "2x3"
#currProbecardSIze = "star"
#currProbecardSIze = "2x8"
#currProbecardSIze = "3x3"
#currProbecardSIze = "4x4"
#currProbecardSIze = "2x16"

#TODO: Which parameter actually decides which dominate Option is better??? Score -> best of worst might be bad. LeastFlex Sum?? -> TODO
if __name__ == "__main__":

    td_scenario_list = {0: (4,3), 1: (3,5), 2: (3,7), 3: (7,3), 4: (6,5)}

    curr_weight = [20, 80, 0]
    weightSettingsObj = WeightSettingsClass(weight_score_gain=curr_weight[0], weight_adjacent_flex_sum=curr_weight[1], weight_forbidden_distance_and_optional_covered_static=curr_weight[2])

    #"Normal" Manuell
    Greedy_Main(currInputMapFilepath, currProbecardSIze, saveResults=False, debugPrint=True, solution_attempts=1, parallelization=False, versionID = curr_versionID, weightSettingsObj=weightSettingsObj, td_scenario_list=td_scenario_list)

    #No Debug Print currInputMapFilepath
    #Greedy_Main(currInputMapFilepath, currProbecardSIze, saveResults=True, debugPrint=False, solution_attempts=1, parallelization=False, versionID = curr_versionID)
    
    # Paralellization for SMALL Debug  filepath_15x15_100Percent filepath_101x101_100Percent
    #Greedy_Main(currInputMapFilepath, currProbecardSIze, saveResults=True, debugPrint=False, parallelization=True, versionID = curr_versionID,
    #           global_timeout_in_seconds = 1800, solution_attempts = 500, max_simultaneous_processes=None) #, max_simultaneous_processes = 2
    
    #Run the Result over and over to compare
    # Instead of chaning the Main Logic. Instead take the Result and calculate HERE, the td_scenario_List for the first n (4) touches, 
    # that cover the highest global TD_count.
    
    exit()

    #Test Dominanz
    #td_list = [[4, 7], [6, 5],[8, 8]]
    #Greedy_Main(currInputMapFilepath, currProbecardSIze, saveResults=False, debugPrint=True, solution_attempts=1, parallelization=False, versionID = curr_versionID ,td_scenario_list= td_list)

    #Generate the Bosch File
    #The Bosch 
    #save_folder="Data_TA660"
    #currInputMapFilepath = "C:/Users/Peter/Desktop/Diplomarbeit_Workspace_Programming/PythonProgramming/DATA/Data_TA660/TA660_2/InputMap_TA660.txt"
    #currProbecardSIze = "2x16_Bosch"

    """
    # LOAD The Device Commander Touchdown List and create the Json Result File
    curr_versionID = None
    SAVE_FOLDER = "Data_TA660"
    #currInputMapFilepath = "C:/Users/Peter/Desktop/Diplomarbeit_Workspace_Programming/PythonProgramming/DATA/Data_TA660/TA660_2/InputMap_TA660.txt"
    currProbecardSIze = "2x16_Bosch"

    curr_td_scenario_list = None
    with open("C:/Users/Peter/Desktop/Diplomarbeit_Workspace_Programming/PythonProgramming/useCasesMaps/td_coordinates_Ta660.txt", 'r') as f:
        curr_td_scenario_list = [eval(line.strip()) for line in f]

    #Mit prev TD list
    Greedy_Main(currInputMapFilepath, currProbecardSIze, td_scenario_list=curr_td_scenario_list, saveResults=True, debugPrint=False, solution_attempts=1, parallelization=False, versionID = curr_versionID, save_folder=SAVE_FOLDER)

    #Multiprocessing selbst ausrechnen...
    Greedy_Main(currInputMapFilepath, currProbecardSIze, saveResults=True, debugPrint=False, parallelization=True, versionID = curr_versionID,
               global_timeout_in_seconds = 1800, solution_attempts = 500, max_simultaneous_processes=None) #, max_simultaneous_processes = 2

    exit()
   """