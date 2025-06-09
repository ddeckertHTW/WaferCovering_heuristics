import numpy as np
import math
import os

#import sys
#myPath = (os.getcwd()+'\\HelperFunc').replace(os.sep, '/')
#sys.path.append(myPath)  # Adjust the path accordingly

#Determines which Subfolder
X_MAX = 15 #Number should be uneven. So that uneven/2 is exactly the center
Y_MAX = X_MAX #Number should be uneven. So that uneven/2 is exactly the center

XY_SIZE_LIST = [15,31,51,101,151,201,251]

DATAPATH = '/Data_Template/'
FOLDER_NAME_ADDITION = '_WaferMap'
# DONT FORGET
#FILE_NAME_ADDITION = '_100Percent_InputMap'
#FILE_NAME_ADDITION = '_Mod4_Error_InputMap'
FILE_NAME_ADDITION = '_Diagonal_Error_InputMap'

def createSphericalArray(x_Max, x_Center, y_Max, y_Center, radius_Value_1, radius_Value_2):
    # Creates a x_Max x y_Max Array. DEFAULT Value is 0. Where from the x_Center/y_Center the distance is measured
    # radius_Value_1 will place 1 by default. radius_Value_2 is added to radius_Value_1 and will place 2 by default
    array = np.zeros((x_Max, y_Max), dtype=int)

    # Loop through each Elem in the array and assing values depending on distance
    for x in range(x_Max):
        for y in range(y_Max):
            distance = np.sqrt((x - x_Center)**2 + (y - y_Center)**2)
            # If the distance is within radius_Value_1, set the value to 1
            if distance < radius_Value_1:
                array[x, y] = 1
            elif distance < radius_Value_2:
                array[x, y] = 2
            #array[x, y] = distance

    return array

def createSphericalArray_Mod4_GridError(x_Max, x_Center, y_Max, y_Center, radius_Value_1, radius_Value_2):
    # Creates a x_Max x y_Max Array. DEFAULT Value is 0. Where from the x_Center/y_Center the distance is measured
    # radius_Value_1 will place 1 by default. radius_Value_2 is added to radius_Value_1 and will place 2 by default
    array = np.zeros((x_Max, y_Max), dtype=int)

    # Loop through each Elem in the array and assing values depending on distance
    for x in range(x_Max):
        for y in range(y_Max):
            distance = np.sqrt((x - x_Center)**2 + (y - y_Center)**2)
            # If the distance is within radius_Value_1, set the value to 1
            if distance < radius_Value_1:
                array[x, y] = 1
            elif distance < radius_Value_2:
                array[x, y] = 2

            # For all x/y that are mod 4 -> Error
            if x%4 == 0 and y%4 == 0:
                array[x, y] = 0


    return array

def createSphericalArray_Diagonal_GridError(x_Max, x_Center, y_Max, y_Center, radius_Value_1, radius_Value_2):
    # Creates a x_Max x y_Max Array. DEFAULT Value is 0. Where from the x_Center/y_Center the distance is measured
    # radius_Value_1 will place 1 by default. radius_Value_2 is added to radius_Value_1 and will place 2 by default
    array = np.zeros((x_Max, y_Max), dtype=int)

    # Loop through each Elem in the array and assing values depending on distance
    for x in range(x_Max):
        for y in range(y_Max):
            distance = np.sqrt((x - x_Center)**2 + (y - y_Center)**2)
            # If the distance is within radius_Value_1, set the value to 1
            if distance < radius_Value_1:
                array[x, y] = 1
            elif distance < radius_Value_2:
                array[x, y] = 2

            # For all x/y that are directly on the diagonal
            if x == y:
                array[x, y] = 0
            if distance < radius_Value_2 and (x+1 == y or x-1 == y):
                array[x, y] = 2

    return array

def createNewFolder(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
            return True
        except OSError as e:
            print(f"Error: {e}")
            return False
    else:
        print(f"Folder '{folder_path}' already exists.")
        return True
    
def safeWaferMap(array,filepath):
    np.savetxt(filepath + ".txt", array, fmt='%d')
    print(f"File: {filepath} created successfully. And saved Array in it.")

def createMain(curr_X_MAX, curr_Y_MAX):
    x_center = math.floor(curr_X_MAX / 2) # Example: If X_MAX = 9 -> Center = 5
    y_center = math.floor(curr_Y_MAX / 2) # Diamater to border is 4 on horzizontal/Vertical. And 5 on diagonal   

    #Different Distances of placement Value 1 / 2
    # Set atleast 2 lower than CENTER to get 0 on the rim
    diameter_value_1 = x_center - 2 # Must be LOWER than DIAMETER_VALUE_2 (it is placed first)
    diameter_value_2 = x_center - 0 # placed second

    #SELECT ERROR LOGIC -  CHANGE NAMING CONSTANT AT TOP!!!
    #array = createSphericalArray(X_MAX, X_CENTER,Y_MAX,Y_CENTER,DIAMETER_VALUE_1,DIAMETER_VALUE_2)
    #array = createSphericalArray_Mod4_GridError(curr_X_MAX, x_center,curr_Y_MAX,y_center,diameter_value_1,diameter_value_2)
    array = createSphericalArray_Diagonal_GridError(curr_X_MAX, x_center,curr_Y_MAX,y_center,diameter_value_1,diameter_value_2)

    dirPath = os.getcwd().replace(os.sep, '/') + DATAPATH + f"{curr_X_MAX}x{curr_Y_MAX}" + FOLDER_NAME_ADDITION
    if(createNewFolder(dirPath)):
        filepath = dirPath + f"/{curr_X_MAX}x{curr_Y_MAX}" + FILE_NAME_ADDITION
        safeWaferMap(array, filepath)



def loopOverAllSizes():
    for size in XY_SIZE_LIST:
        createMain(size, size)

if __name__ == '__main__':
    #loopOverAllSizes()
    createMain(X_MAX, Y_MAX)

