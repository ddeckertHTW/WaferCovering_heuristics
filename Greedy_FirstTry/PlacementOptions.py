import numpy as np
from Greedy_FirstTry.ShapeCoverageMinkowski import get_mask_by_coords, getMapCoordsByMask, getMapValuesByMask
from Greedy_FirstTry.WaferMapClass import WaferMapClass

#Go over the whole Map and determine the placement Options for all MustTouchBins
def get_least_flexible_map_init(waferMapObj: WaferMapClass):
    placeMentOptions = np.zeros_like(waferMapObj.inputMap)

    # currTouchdown is the key of the Dict: (x,y)
    for coords in waferMapObj.getAllMandatoryTouchdowns():
        placeMentOptions[coords[0]][coords[1]] = get_placement_options_count_die(waferMapObj, coords[0], coords[1])

    return placeMentOptions

def get_least_flexible_map_init_strict(waferMapObj: WaferMapClass):
    placeMentOptions = np.zeros_like(waferMapObj.inputMap)

    # currTouchdown is the key of the Dict: (x,y)
    for coords in waferMapObj.getAllMandatoryTouchdowns():
        placeMentOptions[coords[0]][coords[1]] = get_placement_options_count_die_strict(waferMapObj, coords[0], coords[1])
    
    return placeMentOptions



################# FÜR TOUCHDOWN MAP
def updateLeastFlexibleAroundTouchdown_TdMap(waferMapObj: WaferMapClass, touchdownMap, placeMentOptions, x, y):
    #Skip this Function when there are no least Flexible Dies left.
    if(np.all(placeMentOptions == 0)):
        #print("SKIPPED LEAST FLEXIBLE")
        return placeMentOptions
    
    mask = get_mask_by_coords(placeMentOptions, waferMapObj.probecard.mask_1, x, y)
    placeMentOptions[mask] = 0

    # Check Outer Ring (Cover5) 
    coordList = getMapCoordsByMask(placeMentOptions, waferMapObj.probecard.mask_5, x, y)
    for coord in coordList:

        #If touchdown Not even possible -> skip
        if(waferMapObj.is_touchdown_possible_and_mandatory_coords(coord[0],coord[1]) == False):
            continue

        placeMentOptions[coord[0]][coord[1]] = getTouchdownCountForSingleDie_TdMap(waferMapObj, coord[0], coord[1], touchdownMap)

    return placeMentOptions
  
#TODO: Idee -> Also anstatt für jeden Bin einzeln alle möglichkeiten auszuprobieren. Einfach über die FORM iterieren und ein mal 
# für alle checken ob touchdown möglich ist.
def getTouchdownCountForSingleDie_TdMap(waferMapObj: WaferMapClass, x, y, touchdownMap):
    #Loop over the Probecard Sites and use the Offset of each SIte to go over all Placement Options
    count = 0

    for pc_coord in waferMapObj.probecard.binDict.values():
        if(waferMapObj.is_touchdown_possible_coords(x - pc_coord[0], y - pc_coord[1]) == False): #Should inputmap be 1 or not? Otherwise edge pieces are falsly LeastFlexible 1
            continue

        values = getMapValuesByMask(touchdownMap, waferMapObj.probecard.mask_1, x - pc_coord[0], y - pc_coord[1])

        # Len must be same (Border might cut off Values) and all Values in Touchdown Map must be 0.
        if(len(values) == len(waferMapObj.probecard.mask_1.setList) and all(elem == 0 for elem in values)):
            count += 1

    return count

#TODO: UNIFORM
def getTouchdownCountForSingleDie_TdMap_Strict(waferMapObj: WaferMapClass, x, y, touchdownMap, inputMap):
    #Loop over the Probecard Sites and use the Offset of each SIte to go over all Placement Options
    count = 0

    for pc_coord in waferMapObj.probecard.binDict.values():
        if(waferMapObj.is_touchdown_possible_coords(x - pc_coord[0], y - pc_coord[1]) == False): #Should inputmap be 1 or not? Otherwise edge pieces are falsly LeastFlexible 1
            continue

        tdValues = getMapValuesByMask(touchdownMap, waferMapObj.probecard.mask_1, x - pc_coord[0], y - pc_coord[1])
        inputValues = getMapValuesByMask(inputMap, waferMapObj.probecard.mask_1, x - pc_coord[0], y - pc_coord[1])

        # Len must be same (Border might cut off Values) and all Values in Touchdown Map must be 0.
        if(len(tdValues) == len(waferMapObj.probecard.mask_1.setList) and all(elem == 0 for elem in tdValues) and all(elem != 2 for elem in inputValues)):
            count += 1

    return count

def getPossibleTouchdownCoordsToCoverDie(waferMapObj: WaferMapClass, x, y):
    #Loop over the Probecard Sites and use the Offset of each SIte to go over all Placement Options
    coordList = []

    for pc_coord in waferMapObj.probecard.binDict.values():
        if(waferMapObj.is_touchdown_possible_coords(x - pc_coord[0], y - pc_coord[1]) == True): #Should inputmap be 1 or not? Otherwise edge pieces are falsly LeastFlexible 1
            coordList.append((x - pc_coord[0], y - pc_coord[1]))

    return coordList

def getPossibleTouchdownCoordsToCoverDie_NoDouble(waferMapObj: WaferMapClass, x, y, touchdownMap):
    #Loop over the Probecard Sites and use the Offset of each SIte to go over all Placement Options
    coordList = []

    for pc_coord in waferMapObj.probecard.binDict.values():
        if(waferMapObj.is_touchdown_possible_coords(x - pc_coord[0], y - pc_coord[1]) == False): #Should inputmap be 1 or not? Otherwise edge pieces are falsly LeastFlexible 1
            continue

        values = getMapValuesByMask(touchdownMap, waferMapObj.probecard.mask_1, x - pc_coord[0], y - pc_coord[1])

        # Len must be same (Border might cut off Values) and all Values in Touchdown Map must be 0.
        if(len(values) == len(waferMapObj.probecard.mask_1.setList) and all(elem == 0 for elem in values)):
            coordList.append((x - pc_coord[0], y - pc_coord[1]))

    return coordList

def is_td_possible_without_double(waferMapObj: WaferMapClass, x, y, touchdownMap):
    #check if possible and Mandatory and then check if all Values of the (touchdown) Map are 0
    if(waferMapObj.is_touchdown_possible_and_mandatory_coords(x,y) == True):
        values = getMapValuesByMask(touchdownMap, waferMapObj.probecard.mask_1, x, y)
        if(len(values) == len(waferMapObj.probecard.mask_1.setList) and all(elem == 0 for elem in values)):
            return True

    return False

def get_placement_options_count_die(waferMapObj: WaferMapClass, x, y):
    count = 0

    for pc_coord in waferMapObj.probecard.binDict.values():
        if all(val != 0 for val in getMapValuesByMask(waferMapObj.inputMap, waferMapObj.probecard.mask_1,x - pc_coord[0],y - pc_coord[1])):
            count += 1

    """
    #TOTALLY WRONG. ONLY CHECKS THE CURRENT PROBECARD SHAPE. 
    for pc_coord in waferMapObj.probecard.binDict.values():
        if(waferMapObj.is_touchdown_possible_coords(x - pc_coord[0], y - pc_coord[1]) == True):
            count += 1
    """
    return count


def get_placement_options_count_die_strict(waferMapObj: WaferMapClass, x, y):
    count = 0

    for pc_coord in waferMapObj.probecard.binDict.values():
        if all(val == 1 for val in getMapValuesByMask(waferMapObj.inputMap, waferMapObj.probecard.mask_1,x - pc_coord[0],y - pc_coord[1])):
            count += 1

    return count



#coordList = getMapCoordsByMask(self.leastFlexibleBin, waferMapObj.probecard.mask_1, x, y)
#Get all Coordinates that are directly next to a Touchdown. Needs probecard.mask_1 Values as Input
def getAdjacentCoordinates(coordList):
    unique_values = set()
    original_set = set(coordList)

    # Loop through each coordinate
    for x, y in coordList:
        for offset in ([(-1, 0), (1, 0), (0, -1), (0, 1)]):
            unique_values.add((x + offset[0], y + offset[1]))

    # Convert the set to a list (if needed)
    return list(unique_values - original_set)
"""
Test it
testMap = np.zeros_like(self.touchdownMap)
for coord in adjacentCoords:
    testMap[coord] += 1
"""