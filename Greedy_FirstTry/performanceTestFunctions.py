import datetime
import numpy as np
import os
import random
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from WaferMapClass import WaferMapClass
from Greedy_FirstTry.PlacementOptions import getTouchdownCountForSingleDie_TdMap
from HelperFunc.log_Message import fornatTimestampDiff, logMessage, printTimestampDiff
from ProbecardClass import getProbecardByName
from ShapeCoverageMinkowski import getMapCoordsByMask, getMapValuesByMask


filepath = "C:/Users/Peter/Desktop/Diplomarbeit_Workspace_Programming/PythonProgramming/Data_Greedy/151x151_WaferMap/151x151_100Percent_InputMap.txt"
#filepath = "C:/Users/HOP2DR/PycharmProjects/PythonProgramming/Data_Template/151x151_WaferMap/151x151_100Percent_InputMap.txt"
inputMap = np.loadtxt(filepath, dtype=int)  

#  SET SIZE
max_x, max_y = 151, 151
myArrayRandom = np.random.random((max_x, max_y))

arrayCount = np.zeros((max_x, max_y), dtype=int)
for x in range(arrayCount.shape[0]):
    for y in range(arrayCount.shape[1]):
        arrayCount[x][y] = x+y

########SElect arrray To Test
myArray = myArrayRandom
#myArray = arrayCount

#probecardSize = "2x8"
#probecardSize = "2x3"

probecardTestList = ["2x3", "2x8", "2x16", "star"]

loopCount = 10000
loopCount = 50000
loopCount = 100000

loopCount = 10000
#loopCount = 2036046 #Actual Func Calls Count of current Implementation
#x,y = 20,20

###################### INIT STUFF END



def get_masked_values(array, mask, x, y):
    # Calculate absolute indices by adding the current position (x, y) to the mask
    mask_x = mask[:, 0] + x
    mask_y = mask[:, 1] + y

    # Ensure indices are within bounds
    valid_indices = (mask_x >= 0) & (mask_x < array.shape[0]) & (mask_y >= 0) & (mask_y < array.shape[1])
    mask_x = mask_x[valid_indices]
    mask_y = mask_y[valid_indices]
    
    # Retrieve values at masked positions
    values = array[mask_x, mask_y]
    
    return values



def get_masked_coordinates(array, mask, x, y):
    # Calculate absolute indices by adding the current position (x, y) to the mask
    mask_x = mask[:, 0] + x
    mask_y = mask[:, 1] + y

    # Ensure indices are within bounds
    valid_indices = (mask_x >= 0) & (mask_x < array.shape[0]) & (mask_y >= 0) & (mask_y < array.shape[1])
    mask_x = mask_x[valid_indices]
    mask_y = mask_y[valid_indices]
    
    # Retrieve valid coordinates
    coordinates = list(zip(mask_x, mask_y))
    
    return coordinates


def get_masked_coordinates2(array, mask, x, y):
    mask = np.array(mask)
    start_position = np.array((x,y))

    # Add the mask to the starting position
    masked_positions = start_position + mask

    # Filter out coordinates that are out of bounds
    valid_mask = (
        (masked_positions[:, 0] >= 0) & (masked_positions[:, 0] < array.shape[0]) &
        (masked_positions[:, 1] >= 0) & (masked_positions[:, 1] < array.shape[1])
    )

    # Return the valid coordinates
    valid_positions = masked_positions[valid_mask]
    return valid_positions.tolist()


def get_masked_Valuescoordinates(array, mask, x, y):
    # Calculate absolute indices by adding the current position (x, y) to the mask
    mask_x = mask[:, 0] + x
    mask_y = mask[:, 1] + y

    # Ensure indices are within bounds
    valid_indices = (mask_x >= 0) & (mask_x < array.shape[0]) & (mask_y >= 0) & (mask_y < array.shape[1])
    mask_x = mask_x[valid_indices]
    mask_y = mask_y[valid_indices]
    
    # Retrieve valid coordinates
    coordinates = list(zip(mask_x, mask_y))
    values = array[mask_x, mask_y]
    
    return values, coordinates


#Start Main Loop
def Test_Old_CoordsByMask():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        coordList = getMapCoordsByMask(myArray, currMask, x, y)


def Test_Old_ValuesByMask():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        ValueList = getMapValuesByMask(myArray, currMask, x, y)


################## NEW

def Test_New_ValuesByMask():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        valueList2 = get_masked_values(myArray, currMaskArray, x,y)

def Test_New_CoordinatesByMask():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        coordList1 = get_masked_coordinates(myArray, currMaskArray, x,y)

def Test_New_CoordinatesByMask2():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        coordList2 = get_masked_coordinates2(myArray, currMaskArray, x,y)

def Test_New_ValuesCoordinatesByMask():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        values, Coords = get_masked_Valuescoordinates(myArray, currMaskArray, x,y)


#########  LeastFlex Count
def Test_Old_LeastFlex():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        flexCount = getTouchdownCountForSingleDie_TdMap(waferMapObj, x,y, myArray)



### TEST ENUM

def Test_Old_ENUM():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        isTrue = x == InputMapStatus.FORBIDDEN
        isTrue = x == InputMapStatus.MANDATORY
        isTrue = x == InputMapStatus.OPTIONAL

def Test_NEW_ENUM():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        isTrue = x == InputMapStatus.FORBIDDEN.value
        isTrue = x == InputMapStatus.MANDATORY.value
        isTrue = x == InputMapStatus.OPTIONAL.value

######### FIND ELEMENTS IN DIEMAP FASTER

# Define a custom class with a 'value' attribute
class CustomObject:
    def __init__(self, value):
        self.MyValue = value

# Function to find elements with the specified target value
def find_elements_with_value(myMap, target_value):
    result = []
    for obj in np.nditer(myMap, flags=['refs_ok']):
        if obj.item().MyValue == target_value:
            result.append(obj.item())
    return result

# Create a 2D numpy array of CustomObject instances

arrayCustomObject = np.zeros((max_x, max_y), dtype=CustomObject)
for x in range(arrayCustomObject.shape[0]):
    for y in range(arrayCustomObject.shape[1]):
        arrayCustomObject[x][y] = CustomObject(x+y)

#00:01:06.768 - Total Time for: Test_Old_FilterBinMap
#00:11:41.568 - Total Time for: Test_Old_FilterMAXBinMap
#00:02:32.963 - Total Time for: Test_New_FilterBinMap
#00:09:26.802 - Total Time for: Test_New_FilterWithNP
def Test_Old_FilterBinMap():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        bin_list = arrayCustomObject.flatten()
        least_flexible_list = [obj for obj in bin_list if obj.MyValue == x]

def Test_Old_FilterMAXBinMap():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        bin_list = arrayCustomObject.flatten()
        max_value_score = max(obj.MyValue for obj in bin_list)
        score_gain_list = [obj for obj in bin_list if obj.MyValue == max_value_score]

def Test_New_FilterBinMap():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        filtered_list = find_elements_with_value(arrayCustomObject, x)

def Test_New_FilterWithNP():
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        values_array = np.vectorize(lambda obj: obj.MyValue)(arrayCustomObject)
        indices = np.argwhere(values_array == x)


################

def TEST_ALL_CHECK():
    flatArray = myArray.flatten()
    
    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        if all(elem == x for elem in flatArray):
            x = 0

def TEST_ANY_CHECK():
    flatArray = myArray.flatten()

    for currloop in range(loopCount):
        x = random.randint(0, max_x)
        if not any(elem != x for elem in flatArray):
            x = 0

##############
def doTimeComparison(funcList):
    for func in funcList:
        startTime = datetime.datetime.now()
        func()
        printTimestampDiff(startTime, f" - Total Time for: {func.__name__}")


############################

#Is it faster to save the coords and access them than to call getValuesByMask func
def Test_New_ValuesBySavedCoords():
    testMap = np.empty(shape=myArray.shape, dtype=testDie)

    for x, y in np.ndindex(testMap.shape):
        #linkedCoords = [(x + dx, y + dy) for dx, dy in currMaskArray 
        #        if 0 <= x + dx < testMap.shape[0] and 0 <= y + dy < testMap.shape[1]]
        linkedCoords = get_masked_coordinates(myArray, currMaskArray, x,y)
        testMap[x][y] = testDie((x+y), linkedCoords)

    for currloop in range(loopCount):
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)

        values = [myArray[coord[0]][coord[0]] for coord in testMap[x][y].linkedCoords]


class testDie():
    def __init__(self, value, linkedCoords):
        self.value = value
        self.linkedCoords = linkedCoords

"""
Was viele Aufrufe hat: 
    GetValuesByMask
    GetCoordsByMask
    
    GetLeastFlexibleCount
    
    GetSumByMask

    IsTouchdownPossibleWithoutCreatingDoubleTD
    
    
    
    -NP Array mit Object, was meine 20 Maps ersetzt
    LeastFlexible ein mal ausrechnen und dann schauen welcher hash gleich ist
    Für Summe oder Abfragen wäre Referenz/Links/Pointer hammer, damit man nicht immer die gleiche abfrage machen muss
    
    Richtige Python Naming convention
    Enum für was bei den Maps was bedeutet...


    Für parallel Processing schon direkt trennen was main - init - mainloop etc. angeht...
    
    Für Vorgegebene Testpfade oder Auswahl an touchdowns (Rheinfolge) einen einfachen export und inport machen, dass ich an einem Beispiel direkt "neu" starten kann mit gleichen werten
    Rekonstuktion von Ablauf (prints) durch TouchdownLocation List
    
    
    Wie sind Daten zu generieren und speichern bei: 
    Wafermapgrößen: 15x15, 51x51 - Probecard Größe: 2x6, 4x4... - UseCases: Mod4, 100%, Diagonale
    
"""

if __name__ == "__main__":
    startTimeGlobal = datetime.datetime.now()
    probecardSize = "2x8"
    print(loopCount, " - loops")

    if(False):
        probecard = getProbecardByName(probecardSize)
        # SELECT CURRENT MASK
        currMask = probecard.mask_1
        currMaskArray = np.array(currMask.setList)
        Test_New_ValuesByMask()
        printTimestampDiff(startTimeGlobal, f" - Total Time")

    else:
        execution_times = {}

        for probecardSize in probecardTestList:   
            probecard = getProbecardByName(probecardSize)
            # SELECT CURRENT MASK
            currMask = probecard.mask_1
            currMaskArray = np.array(currMask.setList)

            print("Selected Probecard: ", probecardSize)
            ### SELECT FUNCTION TO TEST
            #funcList = [Test_Old_CoordsByMask, Test_New_CoordinatesByMask, Test_New_CoordinatesByMask2, Test_Old_ValuesByMask, Test_New_ValuesByMask, Test_New_ValuesCoordinatesByMask]
            #funcList = [Test_New_ValuesByMask, Test_New_ValuesBySavedCoords]
            #funcList = [Test_Old_ENUM, Test_NEW_ENUM]
            #funcList = [Test_Old_FilterBinMap, Test_Old_FilterMAXBinMap, Test_New_FilterBinMap, Test_New_FilterWithNP]
            #funcList = [Test_Old_FilterBinMap, Test_New_FilterBinMap, Test_New_FilterWithNP]
            funcList = [TEST_ALL_CHECK, TEST_ANY_CHECK]

            waferMapObj = WaferMapClass(myArray, probecard)

            for func in funcList:
                startTimeFunc = datetime.datetime.now()
                func() # Call the func in the List
                printTimestampDiff(startTimeFunc, f" - Total Time for: {func.__name__}")

                #Add time to sum List
                end_time = datetime.datetime.now()
                elapsed_time = end_time - startTimeFunc

                if func.__name__ not in execution_times:
                    execution_times[func.__name__] = datetime.timedelta(0)
                execution_times[func.__name__] += elapsed_time

        print("############# SUM OF TIMES")
        for funcCallName in execution_times:
            print(f"{fornatTimestampDiff(execution_times[funcCallName])} - Function Called: {funcCallName}")

