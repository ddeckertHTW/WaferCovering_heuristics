import numpy as np

from Greedy_FirstTry.probecardCover import probecardMask


#Returns a List. USE: if 0 in values | CHECK: all(x == 0 for x in values)
def getMapValuesByMask_OLD(map: np.array, mask: probecardMask, x, y) -> list:
    # Get the Coordinates of the relevant Bins using the current Cover setList
    new_coordinates = [(x + coord[0], y + coord[1]) for coord in mask.setList]

    # Get the Map Values on the new coordinates. Do not return out of Bounds Elements. (x: -1) would return a false Element here
    values = [map[coord[0], coord[1]] for coord in new_coordinates
              if 0 <= coord[0] < map.shape[0] and 0 <= coord[1] < map.shape[1]]

    return values

#TODO: Effizienter direkt np.all(... == 0) danut abbruch gemacht werden kann

#Returns a List. USE: if 0 in values | CHECK: all(x == 0 for x in values)
def getMapValuesByMask(map: np.array, mask: probecardMask, x, y) -> list:
    new_coordinates = np.array([(x + coords[0], y + coords[1]) for coords in mask.setList])
    
    # Filter out coordinates that are out of bounds
    valid_mask = (new_coordinates[:, 0] >= 0) & (new_coordinates[:, 0] < map.shape[0]) & \
                 (new_coordinates[:, 1] >= 0) & (new_coordinates[:, 1] < map.shape[1])
    
    valid_coordinates = new_coordinates[valid_mask]

    # Extract values using valid coordinates
    values = map[valid_coordinates[:, 0], valid_coordinates[:, 1]]

    return values.tolist()

def getMapValuesByCoordList(map: np.array, coordList) -> list:
    valueList = []

    for coord in coordList:
        valueList.append(map[coord[0]][coord[1]])

    return valueList

def getMapCoordsByMask(map: np.array, mask: probecardMask, x, y) -> list:
    # Get the Coordinates of the relevant Bins using the current Cover setList
    new_coordinates = [(x + coords[0], y + coords[1]) for coords in mask.setList
                        if 0 <= (x + coords[0]) < map.shape[0] and 0 <= (y + coords[1]) < map.shape[1]]

    return new_coordinates

# Return a Map the same size as given Map to act as Boolean indexing. map[mask]
def get_mask_by_coords(map: np.array, cover: probecardMask, x, y):
    # Get the Coordinates of the relevant Bins using the current Cover setList
    coordList = [(x + coords[0], y + coords[1]) for coords in cover.setList
                if 0 <= (x + coords[0]) < map.shape[0] and 0 <= (y + coords[1]) < map.shape[1]]

    mask = np.zeros(map.shape, dtype=bool)

    for coord in coordList:
        mask[coord] = True

    #How to use: filtered_array = map[mask]
    return mask    


#TODO: TESTING FOR Edge Cases, that the Coords are out of Bounds of the Map
# Array will always be NxM Size regardless of probecard Shape. So do: partialMap[cover.coverArray == 1] to only select relevant
# Will return the linked Original Map. So be carefull with changes.
# !!! IF coords are out of Bounds MAP WILL BE WRONG!!!
def getLinkedPartialMapByMask(map: np.array, mask: probecardMask, x, y) -> list:
    # Get the Coordinates of the relevant Bins using the current Cover setList
    coordList = [(x + coords[0], y + coords[1]) for coords in mask.setList
                 if 0 <= (x + coords[0]) < map.shape[0] and 0 <= (y + coords[1]) < map.shape[1]]
    
    #TODO: ERROR : WHat do when Map goes out of bounds???
    xOffset = min(coord[0] for coord in coordList)
    yOffset = min(coord[1] for coord in coordList)

    return map[xOffset: xOffset + mask.xSize, yOffset: yOffset + mask.ySize]

    #For correct Array Size. But will be different than cover...

    rows, cols = zip(*coordList)

    filtered_array = map[rows, cols]

    min_x = min(coord[0] for coord in coordList)
    max_x = max(coord[0] for coord in coordList)
    min_y = min(coord[1] for coord in coordList)
    max_y = max(coord[1] for coord in coordList)

    test = map[min_x: max_x + 1, min_y: max_y + 1]
    test2 = map[xOffset: xOffset + mask.xSize, yOffset: yOffset + mask.ySize]

    return map[min_x: max_x + 1, min_y: max_y + 1]
    """ Alternativer Ansatz
    #TOD O: Look where this is used. If all Elements are set to a Value then it is wrongly used. THERE ARE FILLER ELEMENTS if needed...
    
    #Create a new Empty Array and just fill in the Coords Positions. Not all
    min_x = min(coord[0] for coord in coordList)
    max_x = max(coord[0] for coord in coordList)
    min_y = min(coord[1] for coord in coordList)
    max_y = max(coord[1] for coord in coordList)
    newArray = np.zeros( (max_x - min_x + 1, max_y - min_y + 1), dtype=map.dtype)

    for x, y in coordList:
        newArray[x - min_x, y - min_y] = map[x, y]

    return newArray

    #Or even simpler. But this is a new Array
    #result = np.zeros_like(substractedMap)
    #result[cover.coverArray == 1] = substractedMap[cover.coverArray == 1]


    """

 ##############
def minkowskiSumAllPermutations(A, B):
    sum_set = set()
    for offset_a in A:
        A_Offset = [(x - offset_a[0], y - offset_a[1]) for x, y in A]
        for a in A_Offset:
            for b in B:
                sum_set.add((a[0] + b[0], a[1] + b[1]))

    return list(sum_set)


def minkowskiSubtraction(A, B):
    set_A = set(A)
    set_B = set(B)
    result = set_A - set_B
    return list(result)


# Input: [(0, 1), (1, 1), ...]
# Output: [0, 1] -> A NP Array where the coordinates are 1. The Rest is 0
#         [0, 1] 
def convertListToNpArray(coordList):
    min_x = min(coord[0] for coord in coordList)
    max_x = max(coord[0] for coord in coordList)
    min_y = min(coord[1] for coord in coordList)
    max_y = max(coord[1] for coord in coordList)

    # Calculate dimensions of the output array
    rows = max_x - min_x + 1
    cols = max_y - min_y + 1

    # Create a NumPy array of zeros
    output_array = np.zeros((rows, cols), dtype=int)

    # Mark specified coordinates with value 1
    for coord in coordList:
        adjusted_x = coord[0] - min_x
        adjusted_y = coord[1] - min_y
        output_array[adjusted_x, adjusted_y] = 1

    # Offset of where the "original" 0/0 coord is -> -min_x, -min_y
    return output_array

# Input: [(0, 1), (1, 1), ...]
# Output: [0, 1] -> A NP Array where the coordinates have the value 1. The Rest 0. Offset is the distance to coord (0,0)
#         [0, 1] 
def convertListToNpArray_WithOffset(coordList):
    min_x = min(coord[0] for coord in coordList)
    max_x = max(coord[0] for coord in coordList)
    min_y = min(coord[1] for coord in coordList)
    max_y = max(coord[1] for coord in coordList)

    # Calculate dimensions of the output array
    rows = max_x - min_x + 1
    cols = max_y - min_y + 1

    # Create a NumPy array of zeros
    output_array = np.zeros((rows, cols), dtype=int)

    # Mark specified coordinates with value 1
    for coord in coordList:
        adjusted_x = coord[0] - min_x
        adjusted_y = coord[1] - min_y
        output_array[adjusted_x, adjusted_y] = 1

    # Offset of where the "original" 0/0 coord is -> -min_x, -min_y
    return output_array, min_x, min_y
