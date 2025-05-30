import datetime
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from Load_Safe.check_folder_exists import check_folder_exists
from Load_Safe.removeSolutionFromDir import removeSolutionFromDir
from Load_Safe.get_filepath_Json import get_filepath_Json
from HelperFunc.is_versionID_json_Impossible import is_versionID_json_Impossible
from HelperFunc.is_versionID_json_older import is_file_versionID_older
from HelperFunc.printTimestampDiff import printTimestampDiff
from GreedyMain import Greedy_Main
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass

from inputMapsLibary import filepath_100Percent_Dict, filepath_Diagonal_Error_Dict, filepath_Mod4_Error_Dict
from probecardLibary import probecardDict_ForTesting

scriptFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#IMPORTANT FOR DELETING ONLY OLD FILES. AND NOT NEW ONES. If Version in json Solution is lower -> delete file to regenerate
new_versionID = 11

# Re-Generates all COmbinations of Probecard x InputMap and saves them in the DataFolderPath
if __name__ == "__main__":
    #removeOldMapsFromALLDir(filterFilepath)
    startTime = datetime.datetime.now()

    # filepath_100Percent_Dict | filepath_Diagonal_Error_Dict | filepath_Mod4_Error_Dict
    Folder_MapTypes = {
        "Data_Greedy_100Percent": filepath_100Percent_Dict, 
        "Data_Greedy_Mod4": filepath_Mod4_Error_Dict, 
        "Data_Greedy_Diagonal": filepath_Diagonal_Error_Dict, 
    }

    curr_weight = [20, 80, 0]
    weightSettingsObj = WeightSettingsClass(weight_score_gain=curr_weight[0], weight_adjacent_flex_sum=curr_weight[1], weight_forbidden_distance_and_optional_covered_static=curr_weight[2])
    print(f"[WEIGHT COMBINATION]: Weights:{weightSettingsObj}")

    for folder_name, folder_filepath_dict in Folder_MapTypes.items():
        save_folder = folder_name

        for inputMapFilepath in folder_filepath_dict.values():
            for probecard in probecardDict_ForTesting:
                filepath = get_filepath_Json(inputMapFilepath, probecard, save_folder)
                if(check_folder_exists(filepath) == False): raise Exception(f"The save folder '{os.path.dirname(filepath)}' does not exist.")

                #WE SKIP This Generation Step, if the Version ID of the Solution is atleast same to new_versionID
                if(is_file_versionID_older(filepath, new_versionID) or is_versionID_json_Impossible(filepath)):
                    continue

                #If version is Older, we generate File Anew and delete it to start off
                #removeSolutionFromDir(filepath)

                #1800 sec is 30 min
                Greedy_Main(inputMapFilepath, probecard, saveResults=True, debugPrint=False, save_folder=save_folder,
                            parallelization=True, global_timeout_in_seconds = 7200, solution_attempts = 10000, versionID=new_versionID, weightSettingsObj=weightSettingsObj) #, max_simultaneous_processes = 2


        printTimestampDiff(startTime, f" - Total Time FOR FOLDER: {folder_name}")
    printTimestampDiff(startTime, " - Total Time FOR ALL FOLDERS")


