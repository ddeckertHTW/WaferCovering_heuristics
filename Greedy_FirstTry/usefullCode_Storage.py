PRINT PART OF MAP:

print(convertListToNpArray(getMapCoordsByMask(self.touchdownMap,waferMapObj.probecard.mask_5, x, y )))



# Smaller Method:
#keyOfMaxElem = max(ratingsDict, key=ratingsDict.get)
#maxElem = ratingsDict[(keyOfMaxElem[0], keyOfMaxElem[1])]

#Alternative
#test = max(ratingsDict.values())

import numpy as np


def keywithmaxval(d):
     v = list(d.values())
     k = list(d.keys())
     return k[v.index(max(v))]

def maxValFunc(d):
     v = list(d.values())
     return max(v)


#How to convert map into dict
ratingsDict = {index: value for index, value in np.ndenumerate(ratingsMap)} # How to access: self.binsDict[(2,2)]

#Get all elems where MaxValue
bestTouchdownPos =  {key: value for key, value in ratingsDict.items() if value == max(ratingsDict.values())}


#Get a List of all "Best" Options for next Touchdown.
maxRating = np.max(ratingsMap)

# Creates an Array of Tupels. (x,y) -> (1,2) | To use: inputMap[tuple(maxCoordElem)
maxRatingList = np.argwhere(ratingsMap == maxRating) 

#How to get elements from a np array using Tupel
corresponding_elements = [waferMapObj.inputMap[tuple(maxCoordElem)] for maxCoordElem in maxRatingList]

print("Corresponding elements in array2:")
for element in corresponding_elements:
    print(element)


""" Example Input/Touchdown Maps 15x15
    backupInputMap = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0],
        [0, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 0],
        [0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0],
        [0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0],
        [0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0],
        [0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0],
        [0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0],
        [0, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 0],
        [0, 0, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    exampleTouchdownMap = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
"""
