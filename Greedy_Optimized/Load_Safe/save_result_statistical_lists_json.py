import datetime
import json
import numpy as np

from Greedy_Optimized.Load_Safe.get_versionID import get_versionID
from HelperFunc.is_versionID_json_older import get_Version_ID_For_Print, is_file_versionID_older
from Solution.ResultClass import ResultClass


def get_statistical_values(result_list):
    # Extracting the `myVal` attribute into a list and then convert it to a NumPy array
    #values = np.array([obj.final_score for obj in result_list])
    values = np.array([int(obj.total_time_ms.total_seconds() * 1000)  for obj in result_list])

    #Min / Max
    min = np.min(values)
    max = np.max(values)

    # Mean
    mean = np.mean(values)

    # Median
    median = np.median(values)

    # Range (max - min). Also der spread
    data_range = np.ptp(values)

    # Variance
    variance = np.var(values, ddof=1)  # ddof=1 for sample variance (Bessel's correction)

    # Standard Deviation
    std_dev = np.std(values, ddof=1)

    # Percentiles (e.g., 25th, 50th, and 75th percentiles)
    percentile_01 = np.percentile(values, 1)
    percentile_05 = np.percentile(values, 5)
    percentile_10 = np.percentile(values, 10)
    percentile_25 = np.percentile(values, 25)
    percentile_50 = np.percentile(values, 50)
    percentile_75 = np.percentile(values, 75)
    percentile_90 = np.percentile(values, 90)

    # Mode (manual approach for non-integer data)
    #values2, counts = np.unique(values, return_counts=True)
    #mode = values2[np.argmax(counts)] if np.any(counts > 1) else "No mode"

    #many standard deviations a data point is from the mean of the dataset
    #z_scores = (values - mean) / std_dev

    # The index of when the first best Value appeared
    min_first_index = np.where(values == min)[0][0]

    
    statistics = {
        "min": min,
        "max": max,
        "min_first_index": min_first_index,
        "mean": mean,
        "median": median,
        "range": data_range,
        "variance": variance,
        "std_dev": std_dev,
        "percentile_99": percentile_01,
        "percentile_95": percentile_05,
        "percentile_90": percentile_10,
        "percentile_75": percentile_25,
        "percentile_50": percentile_50,
        "percentile_25": percentile_75,
        "percentile_10": percentile_90,        
    }
    return statistics

def convert_result_Data(result_list):
    data = {
        "statistics": get_statistical_values(result_list), 
        "score_list_len": len(result_list),
#        "score_list": [result.final_score for result in result_list]
        "score_list": [int(result.total_time_ms.total_seconds() * 1000) for result in result_list]
    }

    return data

#Save the raw Result Lists with scores. Also calculate any meaningfull statistical Values here
def save_result_statistical_lists_json(results_dict, saveFilePath, inputMapFilepath, pcSize, solution_attempts, result_loops, totalTime, versionID, message = ""):
    data = {
        "versionID": get_versionID(versionID),

        "result_loops": result_loops,
        "solution_attempts": solution_attempts,
        "actual_result_count": sum([len(results) for results in results_dict.values()]),
        "message": message,
        "time": totalTime,
        "pcSize": pcSize,        
        "inputMap_Name": inputMapFilepath.rsplit('/')[-1], # Just the Name like: 15x15_InputMap.txt OR 15x15_Diagonal_Error_InputMap.txt
        "inputMap_Filepath": (inputMapFilepath.rsplit('/')[-2] + "/" + inputMapFilepath.rsplit('/')[-1]), #Dont include the Base directorys as it changes by device

        #Get statistics of All results together. Equal to flatmap
        "statistics": get_statistical_values([item for results in results_dict.values() for item in results]),
        
        #Duplicate list of all Scores neeedd? Can be extraced from individual_results
        #"score_list": [item.final_score for result in results_dict.values() for item in result], 

        "individual_results": []
    }

    #For every subset of result_list add the statistics and list of Elements.
    for result_list in results_dict.values():
        data["individual_results"].append(convert_result_Data(result_list))


    #For the statistic of the whole elements. Update min_first_index to reflect the average first Index
    min_first_index_List = []
    for result in data["individual_results"]:
        min_first_index_List.append(result["statistics"]["min_first_index"])

    # Update min_first_index of the MAIN Body to reflect the AVERAGE first Index
    data["statistics"]["min_first_index"] = sum(min_first_index_List) / len(min_first_index_List)


    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    #Only save to File, if VersionID is lower. Not if larger or equal. 
    if(is_file_versionID_older(saveFilePath, versionID)):
        print(f"[NOT saving File] - File {fileName_short} VersionID {get_Version_ID_For_Print(saveFilePath)} is higher than current: {versionID}.")
        return
    
    #Use custom Encoder for np Array and Timedelta
    jsonString = json.dumps(data, indent=4, cls=NpEncoder)

    # Save file
    with open(saveFilePath, 'w') as f:
        f.write(jsonString)

    print("[Saved File] - ", fileName_short)


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