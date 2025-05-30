
import json
import os

def is_versionID_json_Impossible(filepath): #save_folder = "Data_Greedy"
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            json_data = json.load(f)

            #If older and has no attribute versionID.
            if 'versionID' not in json_data:
                return False

            versionID = json_data['versionID']
            #Edge Case where None is filled
            if(versionID == None):
                return False

            #Main Purpose            
            if(versionID == 'IMPOSSIBLE'):
                return True
    
    return False

