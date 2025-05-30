
import json
import os


scriptFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Returns True -> File should not be overwritten, because Version in existing file is higher
# Returns False  -> File should be overwritten, because Version is lower
# If VersionID is None -> Flag to always overwrite -> Ignore and return False 
# Naming Alternative: is_file_versionID_older

#def is_file_versionID_older_Greedy(inputMapFilepath, probecard, new_versionID, save_folder):
def is_file_versionID_older(filepath, new_versionID):
    if(new_versionID == None):
        return False
    
    return check_versionID(filepath, new_versionID)

def check_versionID(json_file_path, new_versionID):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)

            #If older and has no attribute versionID.
            if 'versionID' not in json_data:
                return False

            versionID = json_data['versionID']
            
            #Edge Case where None is filled OR it is IMPOSSIBLE Flag or something.
            if(versionID == None or isinstance(versionID, str)):
                return False

            # Normal behavior where Value is larger or equal
            if(versionID >= new_versionID):
                return True
    
    return False

#Just a helper Func
def get_Version_ID_For_Print(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            json_data = json.load(f)
            
            if 'versionID' not in json_data:
                return ""

            return json_data['versionID']

