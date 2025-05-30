import os
import sys
import numpy as np
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE
from Greedy_FirstTry.ShapeCoverageMinkowski import get_mask_by_coords, getMapCoordsByMask, getMapValuesByMask
from Greedy_FirstTry.ProbecardClass import ProbecardClass, get_offset_toSite1
from Greedy_FirstTry.RankingFunction import get_flex_sum_rating, get_touchdown_rating, get_flex_sum_rating2
from Greedy_FirstTry.WaferMapClass import WaferMapClass


# Returns True if touchdown on given x/y coords is possible. False if not
def isTouchdownPossible(inputMap, probecard: ProbecardClass, x, y):
    values = getMapValuesByMask(inputMap, probecard.mask_1, x, y)

    #Out of Bounds -> Elements are missing OR Do not Touch Bin (0) exists
    if(0 in values or len(values) != len(probecard.mask_1.setList)):
        return False

    return True

def isTouchdownPossible_NoOptional(inputMap, probecard: ProbecardClass, x, y):
    values = getMapValuesByMask(inputMap, probecard.mask_1, x, y)

    #Out of Bounds -> Elements are missing OR Do not Touch Bin (0) exists
    if(0 in values or 2 in values or len(values) != len(probecard.mask_1.setList)):
        return False

    return True

# Represents if the touchdown in this coordinate AS SITE 1 would be possible. Not if the die can be covered at all
# Return Map where every 1 represents a possible Touchdown. 0 If not possible
def getAllPossibleTouchdownsMap(inputMap, probecard):
    possiblePlacements = np.zeros_like(inputMap)

    # Go over the Shape (all Elements) and check if Touchdown is possible
    for coords in np.argwhere(inputMap != 0):
        possiblePlacements[coords[0]][coords[1]] = isTouchdownPossible(inputMap, probecard, coords[0], coords[1])

    return possiblePlacements

#Only PURE Touchdowns
def getAllPossibleTouchdowns_Strict_NoOptional(inputMap, probecard):
    possiblePlacements = np.zeros_like(inputMap)

    # Go over the Shape (all Elements) and check if Touchdown is possible
    for coords in np.argwhere(inputMap != 0):
        possiblePlacements[coords[0]][coords[1]] = isTouchdownPossible_NoOptional(inputMap, probecard, coords[0], coords[1])

    return possiblePlacements


def placeTouchdownOnPos(inputMap, currTouchdownMap, probecard: ProbecardClass, x, y):
    if(isTouchdownPossible(inputMap, probecard, x, y) == False):
        debug = getMapValuesByMask(inputMap, probecard.mask_1, x, y)
        print("ILLEGAL TOUCHDOWN DETECTED, InputMap: ", debug)
        exit()
        #Stop the Programm

    #Here this Partial Map is only a Link. So changes to partialMap will change the currTouchdownMap. CHANGE??
    mask = get_mask_by_coords(currTouchdownMap, probecard.mask_1, x, y)
    currTouchdownMap[mask] += 1

    return currTouchdownMap

# Similar to updateLeastFlexibleAroundTouchdown_TdMap - MERGE?
# Get the first Touchdown Location to cover the given bin (coordintaes) WITHOUT creating a double Touchdown. 
def getOnlyTouchdownByCoord(inputMap, currTouchdownMap, probecard: ProbecardClass, x, y): #ONLY POSSIBLE WHEN Coordinate has LeastFlexible == 1
    # Go through all Probecard Sites and test them for beeing the new Site 1 
    for coord in probecard.binDict.values():
        td_values = getMapValuesByMask(currTouchdownMap, probecard.mask_1, x - coord[0], y - coord[1])

        if all(val == 0 for val in td_values):
            coordOffset = get_offset_toSite1(probecard.binDict, coord[0], coord[1])
            if(isTouchdownPossible(inputMap, probecard, x + coordOffset[0], y + coordOffset[1]) == False):
                continue

            return (x + coordOffset[0], y + coordOffset[1])

    raise Exception("ERROR. COULD NOT FIND THE ONLY POSSIBLE PLACEMENT OPTION!!!")


# TODO: THIS IS INEFFICIENT - Rewrite it!!!
# Erster durchlauf: Weil alles noch kein Touchdown hat, kann man einfach 4 oder 3 annehmen jeh nach inputmap

# Without any Touchdowns placed. Rate all possible Touch Locations - This is Step 0
def rateAllPossibleTouchdowns(waferMapObj: WaferMapClass) -> np.ndarray:
    newRatings = np.full_like(waferMapObj.inputMap, IMPOSSIBLE_VALUE_NEGATIVE)

    for coord in waferMapObj.getAllPossibleTouchdowns():
        inputMapValues = getMapValuesByMask(waferMapObj.inputMap, waferMapObj.probecard.mask_1, coord[0],coord[1])
        tdValues = [0] * len(inputMapValues) #tdValues are all 0 at Step 0 !

        newRatings[coord[0]][coord[1]] = get_touchdown_rating(inputMapValues, tdValues)
    
    return newRatings


#Just for initialisation for first Status.
def getAllFlexibleBin_Sum(waferMapObj: WaferMapClass, probecard: ProbecardClass, touchdownMap, leastflexibleStrict):
    sumMap = np.full_like(leastflexibleStrict, IMPOSSIBLE_VALUE_POSITIVE)

    for coord in waferMapObj.getAllPossibleMandatoryTouchdowns():
        sumMap[coord[0]][coord[1]] = get_flex_sum_rating(waferMapObj.inputMap, probecard, leastflexibleStrict, touchdownMap, coord[0], coord[1])

    return sumMap

#Just for initialisation for first Status.
def getAllFlexibleBin_Sum2(waferMapObj: WaferMapClass, probecard: ProbecardClass, touchdownMap, leastflexibleStrict):
    sumMap = np.full_like(leastflexibleStrict, IMPOSSIBLE_VALUE_POSITIVE)

    for coord in waferMapObj.getAllPossibleMandatoryPureTouchdowns():
        sumMap[coord[0]][coord[1]] = get_flex_sum_rating2(waferMapObj.inputMap, probecard, leastflexibleStrict, touchdownMap, coord[0], coord[1])

    return sumMap

#Just for initialisation for first Status.
def getAllFlexibleBin_Sum3(waferMapObj: WaferMapClass, probecard: ProbecardClass, touchdownMap, leastflexibleStrict):
    sumMap = np.full_like(leastflexibleStrict, IMPOSSIBLE_VALUE_POSITIVE)

    for coord in waferMapObj.getAllPossibleTouchdowns():
        sumMap[coord[0]][coord[1]] = get_flex_sum_rating2(waferMapObj.inputMap, probecard, leastflexibleStrict, touchdownMap, coord[0], coord[1])

    return sumMap

def getAllFlexibleStrict_Sum(waferMapObj: WaferMapClass, leastFlexibleBin):
    sumMap = np.zeros_like(leastFlexibleBin)

    #Set Optional TOuch Bins to the SiteCount of the Probecard
    sumMap[waferMapObj.inputMap == 2] = waferMapObj.probecard.sitesCount

    #TODO: Frage LeastFlexible Count soll nicht randstücke als Optionen akzeptieren

    #Loop over every Bin, that has a leastFlexible Rating.
    for coord in np.argwhere(leastFlexibleBin >= 1):
        sumMap[coord[0]][coord[1]] = sum(getMapValuesByMask(leastFlexibleBin, waferMapObj.probecard.mask_1, coord[0], coord[1]))

    return sumMap


####################

# We just need to look at the current correpation of currTouchdownCount [x][y] + 1 * InputMapValue
# Just the differenct of the current Rating of the die and now. So the DELTA
# Ratings Map is just the Rating Delta -> The difference what a Touchdown would add/substract
def updateRatingsAroundTouchdown(waferMapObj: WaferMapClass, ratingsMap, touchdownMap, x, y):
    mask = get_mask_by_coords(ratingsMap, waferMapObj.probecard.mask_1, x, y)
    maskMap3 = ratingsMap[mask]

    # Check Cover 3 -> Pc + Pc .Skip x/y touchdown as it will be IMPOSSIBLE_VALUE_NEGATIVE anyway
    coordList = getMapCoordsByMask(ratingsMap, waferMapObj.probecard.mask_3, x, y)
    for coord in coordList:
        #If touchdown Not even possible -> skip
        if(waferMapObj.is_touchdown_possible_coords(coord[0],coord[1]) == False):
            continue
        
        tdValues = getMapValuesByMask(touchdownMap, waferMapObj.probecard.mask_1, coord[0],coord[1])
        inputMapValues = getMapValuesByMask(waferMapObj.inputMap, waferMapObj.probecard.mask_1, coord[0],coord[1])

        ratingsMap[coord[0]][coord[1]] = get_touchdown_rating(inputMapValues, tdValues)

    return ratingsMap

