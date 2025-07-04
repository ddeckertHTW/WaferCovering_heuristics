
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.insert(0, parent_dir)

from GlobalConstants import BASE_DATA_FILEPATH, BASE_GREEDY_FILEPATH

# Kinda Janky, because the middle Save Folder is extracted by the current given InputMap. 
# As Greedy Filepaths are saved in: PythonProgramming/Data_Template/15x15_WaferMap/15x15_100Percent_InputMap.txt - 15x15_WaferMap is extraced as folder
def get_filepath_Json(inputMapFilepath, probecardSize, save_folder, name_addition = ""):
    if name_addition != "":
        name_addition = "_" + name_addition

    if save_folder is None:
        save_folder = get_new_folder_from_path(inputMapFilepath)
        
    return os.path.join(BASE_GREEDY_FILEPATH, save_folder, inputMapFilepath.rsplit('/')[-2], probecardSize + name_addition + ".json").replace("\\", "/")
    

def get_new_folder_from_path(path: str) -> str:
    if "100Percent_InputMap" in path:
        return "Complete"
    elif "Diagonal_Error_InputMap" in path:
        return "Contamination"
    elif "Mod4_Error_InputMap" in path:
        return "TestStructures"
    else:
        raise ValueError("Unknown file type in path.")
