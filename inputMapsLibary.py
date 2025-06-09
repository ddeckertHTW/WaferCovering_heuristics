import os
# Libary/List of all relevant filapths to  InputMaps / USecases. Import this instead of hardcoded Paths in each File seperately

#Only works, because this file is in root / no subfolder
root_dir_path = os.path.dirname(os.path.abspath(__file__))

filepath_15x15_100Percent = root_dir_path + "/Data_Template/15x15_WaferMap/15x15_100Percent_InputMap.txt"
filepath_31x31_100Percent = root_dir_path + "/Data_Template/31x31_WaferMap/31x31_100Percent_InputMap.txt"
filepath_51x51_100Percent = root_dir_path + "/Data_Template/51x51_WaferMap/51x51_100Percent_InputMap.txt"
filepath_101x101_100Percent = root_dir_path + "/Data_Template/101x101_WaferMap/101x101_100Percent_InputMap.txt"
filepath_151x151_100Percent = root_dir_path + "/Data_Template/151x151_WaferMap/151x151_100Percent_InputMap.txt"
filepath_201x201_100Percent = root_dir_path + "/Data_Template/201x201_WaferMap/201x201_100Percent_InputMap.txt"
filepath_251x251_100Percent = root_dir_path + "/Data_Template/251x251_WaferMap/251x251_100Percent_InputMap.txt"

#Diagonal Errors - 15x15_Diagonal_Error_InputMap
filepath_15x15_Diagonal_Error = root_dir_path + "/Data_Template/15x15_WaferMap/15x15_Diagonal_Error_InputMap.txt"
filepath_31x31_Diagonal_Error = root_dir_path + "/Data_Template/31x31_WaferMap/31x31_Diagonal_Error_InputMap.txt"
filepath_51x51_Diagonal_Error = root_dir_path + "/Data_Template/51x51_WaferMap/51x51_Diagonal_Error_InputMap.txt"
filepath_101x101_Diagonal_Error = root_dir_path + "/Data_Template/101x101_WaferMap/101x101_Diagonal_Error_InputMap.txt"
filepath_151x151_Diagonal_Error = root_dir_path + "/Data_Template/151x151_WaferMap/151x151_Diagonal_Error_InputMap.txt"
filepath_201x201_Diagonal_Error = root_dir_path + "/Data_Template/201x201_WaferMap/201x201_Diagonal_Error_InputMap.txt"
filepath_251x251_Diagonal_Error = root_dir_path + "/Data_Template/251x251_WaferMap/251x251_Diagonal_Error_InputMap.txt"

#Mod 4 Errors
filepath_15x15_Mod4_Error = root_dir_path + "/Data_Template/15x15_WaferMap/15x15_Mod4_Error_InputMap.txt"
filepath_31x31_Mod4_Error = root_dir_path + "/Data_Template/31x31_WaferMap/31x31_Mod4_Error_InputMap.txt"
filepath_51x51_Mod4_Error = root_dir_path + "/Data_Template/51x51_WaferMap/51x51_Mod4_Error_InputMap.txt"
filepath_101x101_Mod4_Error = root_dir_path + "/Data_Template/101x101_WaferMap/101x101_Mod4_Error_InputMap.txt"
filepath_151x151_Mod4_Error = root_dir_path + "/Data_Template/151x151_WaferMap/151x151_Mod4_Error_InputMap.txt"
filepath_201x201_Mod4_Error = root_dir_path + "/Data_Template/201x201_WaferMap/201x201_Mod4_Error_InputMap.txt"
filepath_251x251_Mod4_Error = root_dir_path + "/Data_Template/251x251_WaferMap/251x251_Mod4_Error_InputMap.txt"

# ForTesting
filepath_100Percent_Dict = {
    '15x15': filepath_15x15_100Percent,
    '31x31': filepath_31x31_100Percent,
    '51x51': filepath_51x51_100Percent,
    '101x101': filepath_101x101_100Percent,
    '151x151': filepath_151x151_100Percent,
    #'201x201': filepath_201x201_100Percent,
    #'251x261': filepath_251x251_100Percent,
}

filepath_Diagonal_Error_Dict = {
    '15x15': filepath_15x15_Diagonal_Error,
    '31x31': filepath_31x31_Diagonal_Error,
    '51x51': filepath_51x51_Diagonal_Error,
    '101x101': filepath_101x101_Diagonal_Error,
    '151x151': filepath_151x151_Diagonal_Error,
    #'201x201': filepath_201x201_Diagonal_Error,
    #'251x261': filepath_251x251_Diagonal_Error,
}

filepath_Mod4_Error_Dict = {
    '15x15': filepath_15x15_Mod4_Error,
    '31x31': filepath_31x31_Mod4_Error,
    '51x51': filepath_51x51_Mod4_Error,
    '101x101': filepath_101x101_Mod4_Error,
    '151x151': filepath_151x151_Mod4_Error,
    #'201x201': filepath_201x201_Mod4_Error,
    #'251x261': filepath_251x251_Mod4_Error,
}

#A Smaller Version for CSP
filepath_100Percent_Dict_small = {
    '15x15': filepath_15x15_100Percent,
    '31x31': filepath_31x31_100Percent,
    '51x51': filepath_51x51_100Percent,
    '101x101': filepath_101x101_100Percent,
    #'151x151': filepath_151x151_100Percent,

}

filepath_Diagonal_Error_Dict_small = {
    '15x15': filepath_15x15_Diagonal_Error,
    '31x31': filepath_31x31_Diagonal_Error,
    '51x51': filepath_51x51_Diagonal_Error,
    '101x101': filepath_101x101_Diagonal_Error,
    #'151x151': filepath_151x151_Diagonal_Error,

}

filepath_Mod4_Error_Dict_small = {
    '15x15': filepath_15x15_Mod4_Error,
    '31x31': filepath_31x31_Mod4_Error,
    '51x51': filepath_51x51_Mod4_Error,
    '101x101': filepath_101x101_Mod4_Error,
    #'151x151': filepath_151x151_Mod4_Error,

}


filepaths_Gif_Worthy = [
    filepath_15x15_100Percent,
    filepath_15x15_Diagonal_Error,
    filepath_15x15_Mod4_Error,
    filepath_31x31_100Percent,
    filepath_31x31_Diagonal_Error,
    filepath_31x31_Mod4_Error,
    filepath_51x51_100Percent,
    filepath_51x51_Diagonal_Error,
    filepath_51x51_Mod4_Error,
]

filepaths_Gif_Worthy_extended = [
    filepath_101x101_100Percent,
    filepath_101x101_Diagonal_Error,
    filepath_101x101_Mod4_Error,
    filepath_151x151_100Percent,
    filepath_151x151_Diagonal_Error,
    filepath_151x151_Mod4_Error,
]