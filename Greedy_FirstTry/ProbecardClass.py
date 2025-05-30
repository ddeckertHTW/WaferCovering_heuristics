import numpy as np

from Greedy_FirstTry.probecardCover import probecardMask
from Greedy_FirstTry.ShapeCoverageMinkowski import convertListToNpArray_WithOffset, minkowskiSumAllPermutations, minkowskiSubtraction


#from probecardLibary import probecardDict
#from ...PythonProgramming.probecardLibary import probecardDict

#TODO: Range ist manchmal inclusiv / exclusiv. Bessere Namen/Beide Versionen Abbilden!!!
class ProbecardClass:
    def __init__(self, probecard):
        #Sanity Check for Probecard Format.
        check_probecard_dimensions(probecard)
        probecard = adjust_probecard_corrds(probecard)

        #USE:     for key in sorted(probecard.binDict.keys()):
        #Create dictionary with SiteID as Key. Example: (1,5,2) -> (x:1, y:5, siteId: 2)
        self.binDict = {point[2]: (point[0], point[1]) for point in probecard}
        self.sitesCount = len(probecard)


        #Calculate helping Variables of x/y Values
        x_values = [point[0] for point in probecard]
        y_values = [point[1] for point in probecard]
    
        self.x_size = max(x_values) - min(x_values)
        self.y_size = max(y_values) - min(y_values)

        # With Range we want to include the bounary to be able to do range(0,x_range). We have to add 1. 
        self.x_range = self.x_size + 1 
        self.y_range = self.y_size + 1

        # Masks using Minkowski SUms
        # Pc | Just the Mask of the Probecard itself
        self.mask_1 = getProbecard_mask_1(self.binDict.values())
        #print("Mask1 Array: \n", self.mask_1.coverArray)

        # Pc around a single Die
        self.mask_2 = getProbecard_mask_2(self.binDict.values())
        #print("Mask2 Array: \n", self.mask_2.coverArray)

        # Pc + Pc | Pc around a Probecard
        self.mask_3 = getProbecard_mask_3(self.binDict.values())
        #print("Mask3 Array: \n", self.mask_3.coverArray)

        # Pc + Pc + Pc | The Mask for all elements that are needed for all relevant Informations after a Touchdown
        self.mask_4 = getProbecard_mask_4(self.binDict.values(), self.mask_3.setList)
        #print("Mask5 Array: ", self.mask_4.coverArray)

        # Pc + Pc - Pc | The Mask for all OUTER Elements of Mask1 (substracted by inner Mask0)
        self.mask_5 = getProbecard_mask_5(self.binDict.values(), self.mask_3.setList)
        #print("Mask5 Array: \n", self.mask_5.coverArray)

        # Adjacent coordinates to a touchdown | The Mask for the Site1 Coordinates to find adjacent coords
        self.mask_adjacent = getProbecard_mask_adjacent(list(self.binDict.values()), self.mask_1, self.mask_4.setList)
        #print("mask_adjacent Array: \n", self.mask_adjacent.coverArray)

        #print()

        #Helper Array. Can delete
        """
        debugArray = np.zeros((self.x_size + 1, self.y_size + 1), dtype=int)
        for x, y, z in probecard:
            debugArray[x - min(x_values), y - min(y_values)] = 1
        """


#Return absolute (x,y) Coord OFfset to the Site1 where we place the Touchdowns
def get_offset_toSite1(binDict, x, y):
    site_1_coords = binDict.get(min(binDict.keys()))
    return (site_1_coords[0] - x, site_1_coords[1] - y)
        
"""

Mask1 Array: 
 [[0 1 0]
 [1 1 1]
 [0 1 0]]
Mask2 Array:
 [[0 0 1 0 0]
 [0 1 1 1 0]
 [1 1 1 1 1]
 [0 1 1 1 0]
 [0 0 1 0 0]]
Mask3 Array:
 [[0 0 0 1 0 0 0]
 [0 0 1 1 1 0 0]
 [0 1 1 1 1 1 0]
 [1 1 1 1 1 1 1]
 [0 1 1 1 1 1 0]
 [0 0 1 1 1 0 0]
 [0 0 0 1 0 0 0]]
Mask4 Array:  
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
Mask5 Array:
 [[0 0 0 1 0 0 0]
 [0 0 1 1 1 0 0]
 [0 1 1 0 1 1 0]
 [1 1 0 0 0 1 1]
 [0 1 1 0 1 1 0]
 [0 0 1 1 1 0 0]
 [0 0 0 1 0 0 0]]

 mask_adjacent Array: 
 [[0 0 0 1 0 0 0]
 [0 0 1 0 1 0 0]
 [0 1 0 0 0 1 0]
 [1 0 0 0 0 0 1]
 [0 1 0 0 0 1 0]
 [0 0 1 0 1 0 0]
 [0 0 0 1 0 0 0]]
 """


############## Helper Func
def check_probecard_dimensions(pc):
    if all(len(item) == 3 for item in pc):
        return True
    elif all(len(item) == 2 for item in pc):
        raise NotImplementedError("Fix current Probecard and Add SiteIds")
    else:
        raise IndexError("Probecard does not have expected 3-dimensional tuples (SiteIds). Example: (1,5,2) -> (x:1, y:5, siteId: 2)")

# Site 1 should be at coords 0/0 to make things easy. Find SiteID 1 and take that as offset for the whole probecard Array
def adjust_probecard_corrds(pc):
    globalOffset = next(elem for elem in pc if elem[2] == 1)
    return [(elem[0] - globalOffset[0], elem[1] - globalOffset[1], elem[2]) for elem in pc]



# LOAD IN PROBECARD
def getProbecardByName(size):
    # The given String e.g. "2x2" must be present in the probecardLibary.py probecardDict Elem
    from probecardLibary import probecardDict
    return ProbecardClass(probecardDict[size])

### CALC MaskS

#Probecard Mask exactly like the Probecard Shape
def getProbecard_mask_1(pcList):
    maskArray, xOffset, yOffset =  convertListToNpArray_WithOffset(pcList)
    return probecardMask(maskArray, list(pcList), xOffset, yOffset)

#Probecard around a single DIE. 
def getProbecard_mask_2(pcList):
    setList =  minkowskiSumAllPermutations(pcList, [(0,0)])
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)
    return probecardMask(maskArray, setList, xOffset, yOffset)


#Probecard * Probecard -> Probecard Shape AROUND a Probecard. to get all elements that are "affected" by a change within the Probecard.
def getProbecard_mask_3(pcList):
    setList =  minkowskiSumAllPermutations(pcList, pcList)
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)
    return probecardMask(maskArray, setList, xOffset, yOffset)

# Probecard * Probecard * Probecard
def getProbecard_mask_4(pcList, mask_3_set):
    setList =  minkowskiSumAllPermutations(pcList, mask_3_set)
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)

    return probecardMask(maskArray, setList, xOffset, yOffset)

# Probecard * Probecard - Probecard -> So only the outer Slice. Inner is substracted
def getProbecard_mask_5(pcList, mask_3_Set):
    setList =  minkowskiSubtraction(mask_3_Set, pcList)
    maskArray, xOffset, yOffset = convertListToNpArray_WithOffset(setList)

    return probecardMask(maskArray, setList, xOffset, yOffset)

# Adjacent coordinates to a touchdown | The Mask for the Site1 Coordinates to find adjacent coords
def getProbecard_mask_adjacent(pcList, mask1, mask_4_Set):
    #If ANY element of list1 is within List2 -> return True
    def anyMatchInList(list1, list2):
        for coord in list1:
            if coord in list2:
                return True
        return False
    
    #First get the coordinates that are direktly next to any Probecard Site
    from Greedy_FirstTry.PlacementOptions import getAdjacentCoordinates
    adjacentCoords = getAdjacentCoordinates(mask1.setList) 

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
   
    return probecardMask(maskArray, list(mask_coords), xOffset , yOffset)

