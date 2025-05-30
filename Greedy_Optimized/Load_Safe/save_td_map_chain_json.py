import datetime
import json
import numpy as np

from Greedy_Optimized.HelperFunc.is_versionID_json_older import get_Version_ID_For_Print, is_file_versionID_older  

def checkVersionID(versionID):
    if versionID == None:
        return 0
    return versionID
    
def get_TD_count_dict(touchdown_map):
    filtered_values = touchdown_map[np.where(touchdown_map != 0)]
    unique_values, counts = np.unique(filtered_values, return_counts=True)
    return dict(zip(unique_values, counts))


def save_td_map_chain_json(tdMap_List, tdMap_Sum_List, saveFilePath, versionID):
    data = {
        "versionID": checkVersionID(versionID), #"versionID": versionID, 

        "Generated Iterations": tdMap_List.__len__(),
        "td_dict_last_Map": str(get_TD_count_dict(tdMap_Sum_List[len(tdMap_Sum_List) - 1]))
    }

    for i, array in enumerate(tdMap_Sum_List):
        data["td_dict_Sum_Map_"+str(i)] = str(get_TD_count_dict(tdMap_Sum_List[i]))


    for i, array in enumerate(tdMap_List):
        data["TD_Map_"+str(i)] = array

    for i, array in enumerate(tdMap_Sum_List):
        data["TD_Sum_Map_"+str(i)] = array

    #Use custom Encoder for np Array and Timedelta
    jsonString = json.dumps(data, indent=4, cls=NpEncoder)

    #Make the 2D np Arrays readable in the file by formating
    formatted_json_str = jsonString.replace('[\n            ', '[').replace('\n        ]', ']').replace(',\n            ', ', ')

    #For Printing
    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    #Only save to File, if VersionID is lower. Not if larger or equal. 
    if(is_file_versionID_older(saveFilePath, versionID)):
        print(f"[NOT saving File] - File {fileName_short} VersionID {get_Version_ID_For_Print(saveFilePath)} is higher than current: {versionID}.")
        return
    
    # Save file
    with open(saveFilePath, 'w') as f:
        f.write(formatted_json_str)

    print("Saved File: ", saveFilePath)
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