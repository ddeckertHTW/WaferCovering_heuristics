import datetime
import json

import numpy as np


def saveResultJson(tdMap, tdLocations, tdLocationsList, 
               rating, tdCount, time, pcSize, inputMapFilepath, 
               saveFilePath, solution_attempts):
    data = {
        "tdCount": tdCount,
        "rating": rating,
        "time": time,
        "SolutionAttempts": solution_attempts,
        "pcSize": pcSize,
        "inputMapFilepath": inputMapFilepath,

        "tdMap": tdMap,
        "tdLocations": tdLocations,
        "tdLocationsList": tdLocationsList,
    }
    
    #Use custom Encoder for np Array and Timedelta
    jsonString = json.dumps(data, indent=4, cls=NpEncoder)
    #Make the 2D np Arrays readable in the file by formating
    formatted_json_str = jsonString.replace('[\n            ', '[').replace('\n        ]', ']').replace(',\n            ', ', ')

    # Save file
    with open(saveFilePath + ".json", 'w') as f:
        f.write(formatted_json_str)

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