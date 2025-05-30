import json

from Greedy_Optimized.HelperFunc.is_versionID_json_older import get_Version_ID_For_Print, is_file_versionID_older


def save_impossible_solution_json(saveFilePath, versionID, message = ""):
    data = {
        "versionID": "IMPOSSIBLE"
    }
    
    if (message != ""):
        data = {
            "versionID": "IMPOSSIBLE",
            "message": message
        } 

    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    if(is_file_versionID_older(saveFilePath, versionID)):
        print(f"[NOT saving File] - File {fileName_short} VersionID {get_Version_ID_For_Print(saveFilePath)} is higher than current: {versionID}.")
        return

    #Use custom Encoder for np Array and Timedelta
    jsonString = json.dumps(data, indent=4)

    with open(saveFilePath, 'w') as f:
        f.write(jsonString)

    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    print(f"Saved IMPOSSIBLE SOLUTION FLAG File: - {fileName_short}")

