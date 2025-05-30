import json
import os

#Returns None if file does not exist or versionID does not exist in it.
#Otherwise returns the json Object
def load_json_data(filepath):
    if filepath is None:
        return None
         
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            json_data = json.load(f)

            if 'versionID' not in json_data:
                return None

            return json_data
        
    print(f"json File {filepath} does not exists.")
    return None