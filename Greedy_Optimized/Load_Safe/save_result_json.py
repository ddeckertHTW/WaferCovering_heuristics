import datetime
import json
import numpy as np

from Greedy_Optimized.HelperFunc.is_versionID_json_older import get_Version_ID_For_Print, is_file_versionID_older
from Greedy_Optimized.Solution.ResultClass import ResultClass
    
def checkVersionID(versionID):
    if versionID == None:
        return 0
    return versionID
    

def save_result_json(resultObj: ResultClass, inputMap_filepath, pcSize, saveFilePath, totalTime, solution_attempts, finished_attempts, versionID):
    data = {
        "versionID": checkVersionID(versionID), #"versionID": versionID, 

        "score": resultObj.final_score,
        "score_All": resultObj.final_score_All,

        "rating": str(resultObj.Rating_Mandatory),
        "rating_Percentages": str(resultObj.Rating_Mandatory_Percentages),
        "rating_All": str(resultObj.Rating_All),

        "td_Count": resultObj.td_Count,
        "td_Sum": resultObj.td_sum_Mandatory,
        "td_Sum_All": resultObj.td_sum_All,

        "time": resultObj.total_time_ms, #time_sec??
        "time_all_attempts": totalTime,
        "finished_attempts": finished_attempts,
        "solution_attempts": solution_attempts,

        "removed_redundant_Tds": resultObj.redundant_Tds, 

        "pcSize": pcSize,
        "inputMap_Name": inputMap_filepath.rsplit('/')[-1], # Just the Name like: 15x15_InputMap.txt OR 15x15_Diagonal_Error_InputMap.txt
        "inputMap_Filepath": (inputMap_filepath.rsplit('/')[-2] + "/" + inputMap_filepath.rsplit('/')[-1]), #Dont include the Base directorys as it changes by device

        "tdMap": resultObj.touchdown_map,
        "tdLocations": resultObj.touchdown_location_map,
        "tdLocationsList": resultObj.td_Location_List,
    }
    
    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    #Only save to File, if VersionID is lower. Not if larger or equal. 
    if(is_file_versionID_older(saveFilePath, versionID)):
        print(f"[NOT saving File] - File {fileName_short} VersionID {get_Version_ID_For_Print(saveFilePath)} is higher than current: {versionID}.")
        return
    
    #Use custom Encoder for np Array and Timedelta
    jsonString = json.dumps(data, indent=4, cls=NpEncoder)

    #Make the 2D np Arrays readable in the file by formating
    formatted_json_str = jsonString.replace('[\n            ', '[').replace('\n        ]', ']').replace(',\n            ', ', ')

    # Save file
    with open(saveFilePath, 'w') as f:
        f.write(formatted_json_str)

    print("[Saved File] - ", fileName_short)
    #if(debugPrint): print("Saved File: ", fileName_short)
    
    # How to load the data
    #with open('data_file.json', 'r') as f:
    #    loaded_data = json.load(f)


#https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        #Also the Timestamps or Timedelta
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()  
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()  
        return super(NpEncoder, self).default(obj)