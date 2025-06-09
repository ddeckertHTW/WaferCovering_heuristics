from Greedy_Optimized.NPMaskOperations.minkowskiSubtraction import minkowskiSubtraction
from Greedy_Optimized.NPMaskOperations.minkowskiSumAllPermutations import minkowskiSumAllPermutations
from Greedy_Optimized.Probecard.ProbecardMaskClass import ProbecardMaskClass
from Greedy_Optimized.NPOperations.convertListToNpArray_WithOffset import convertListToNpArray_WithOffset

#Probecard Mask exactly like the Probecard Shape
def create_probecard_mask_1(pcList) -> ProbecardMaskClass: 
    maskArray, xOffset, yOffset =  convertListToNpArray_WithOffset(pcList)
    return ProbecardMaskClass(maskArray, list(pcList), xOffset, yOffset)
""" Mask1 Array: 
 [[0 1 0]
 [1 1 1]
 [0 1 0]]
 """
#Probecard around a single DIE. 
def create_probecard_mask_2(pcList) -> ProbecardMaskClass:
    setList =  minkowskiSumAllPermutations(pcList, [(0,0)])
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)
    return ProbecardMaskClass(maskArray, setList, xOffset, yOffset)
""" Mask2 Array:
 [[0 0 1 0 0]
 [0 1 1 1 0]
 [1 1 1 1 1]
 [0 1 1 1 0]
 [0 0 1 0 0]]
"""
#Probecard * Probecard -> Probecard Shape AROUND a Probecard. to get all elements that are "affected" by a change within the Probecard.
def create_probecard_mask_3(pcList) -> ProbecardMaskClass:
    setList =  minkowskiSumAllPermutations(pcList, pcList)
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)
    return ProbecardMaskClass(maskArray, setList, xOffset, yOffset)
""" Mask3 Array:
 [[0 0 0 1 0 0 0]
 [0 0 1 1 1 0 0]
 [0 1 1 1 1 1 0]
 [1 1 1 1 1 1 1]
 [0 1 1 1 1 1 0]
 [0 0 1 1 1 0 0]
 [0 0 0 1 0 0 0]]
"""
# Probecard * Probecard * Probecard
def create_probecard_mask_4(pcList, mask_3_set) -> ProbecardMaskClass:
    setList =  minkowskiSumAllPermutations(pcList, mask_3_set)
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)

    return ProbecardMaskClass(maskArray, setList, xOffset, yOffset)
""" Mask4 Array:  
[[0 0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 1 1 1 0 0 0 0]
 [0 0 0 1 1 1 1 1 0 0 0]
 [0 0 1 1 1 1 1 1 1 0 0]
 [0 1 1 1 1 1 1 1 1 1 0]
 [1 1 1 1 1 1 1 1 1 1 1]
 [0 1 1 1 1 1 1 1 1 1 0]
 [0 0 1 1 1 1 1 1 1 0 0]
 [0 0 0 1 1 1 1 1 0 0 0]
 [0 0 0 0 1 1 1 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0 0]]
"""
# Probecard * Probecard - Probecard -> So only the outer Slice. Inner is substracted
def create_probecard_mask_5(pcList, mask_3_Set) -> ProbecardMaskClass:
    setList =  minkowskiSubtraction(mask_3_Set, pcList)
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)

    return ProbecardMaskClass(maskArray, setList, xOffset, yOffset)
""" Mask5 Array:
 [[0 0 0 1 0 0 0]
 [0 0 1 1 1 0 0]
 [0 1 1 0 1 1 0]
 [1 1 0 0 0 1 1]
 [0 1 1 0 1 1 0]
 [0 0 1 1 1 0 0]
 [0 0 0 1 0 0 0]]
"""

# Probecard * Probecard * Probecard- Probecard -> So only the outer Slice. Inner is substracted
def create_probecard_mask_6(mask_3_Set, mask_4_Set) -> ProbecardMaskClass:
    setList =  minkowskiSubtraction(mask_4_Set, mask_3_Set)
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)

    return ProbecardMaskClass(maskArray, setList, xOffset, yOffset)
""" Mask6 Array: 
 [[0 0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 1 1 1 0 0 0 0]
 [0 0 0 1 1 0 1 1 0 0 0]
 [0 0 1 1 0 0 0 1 1 0 0]
 [0 1 1 0 0 0 0 0 1 1 0]
 [1 1 0 0 0 0 0 0 0 1 1]
 [0 1 1 0 0 0 0 0 1 1 0]
 [0 0 1 1 0 0 0 1 1 0 0]
 [0 0 0 1 1 0 1 1 0 0 0]
 [0 0 0 0 1 1 1 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0 0]]
 """
# Adjacent coordinates to a touchdown | The Mask for the Site1 Coordinates to find adjacent coords
def create_probecard_mask_adjacent(pcList, mask1: ProbecardMaskClass, mask_4_Set) -> ProbecardMaskClass:
    #If ANY element of list1 is within List2 -> return True
    def anyMatchInList(list1, list2):
        for coord in list1:
            if coord in list2:
                return True
        return False
    
    #First get the coordinates that are direktly next to any Probecard Site
    adjacentCoords = getAdjacentCoordinates(mask1.set_list) 

    #The coordinates of Site1 Elements. As Set to be distinct
    mask_coords = set()
    #Take coord as Site1 and check via Probecard coordinates if all elements of that Site1 Touchdown are not overlaping with probecard. BUT any element is adjacent COord
    for coord in mask_4_Set:
        coordList = []
        for pc_offset in pcList:
            coordList.append((coord[0] + pc_offset[0], coord[1] + pc_offset[1]))

        if anyMatchInList(coordList, adjacentCoords) and not anyMatchInList(coordList, pcList):
            mask_coords.add(coord)

    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(mask_coords)
   
    return ProbecardMaskClass(maskArray, list(mask_coords), xOffset , yOffset)


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
