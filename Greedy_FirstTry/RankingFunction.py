import numpy as np

from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE
from Greedy_FirstTry.ProbecardClass import ProbecardClass
from Greedy_FirstTry.ShapeCoverageMinkowski import getMapValuesByMask


# To avoid incrementing the touchdown Map every time. "Atrificially" add 1 to the TouchdownMap Values
def get_touchdown_rating(inputValues, touchdownValues) -> int:
    #If Touchdown is on a 0 on InputMap -> NOT ALLOWED
    if(0 in inputValues): 
        return IMPOSSIBLE_VALUE_NEGATIVE

    #If every bin We are about to Touch allready got a touchdown -> No new Bins -> No GAIN
    if(0 not in touchdownValues):
        return IMPOSSIBLE_VALUE_NEGATIVE

    #There needs to be atleast 1 Must touch die, that is not allready touched. 
    if(any(inputValues[x] == 1 and touchdownValues[x] == 0 for x in range(len(inputValues))) == False):
        return IMPOSSIBLE_VALUE_NEGATIVE

    currRating = 0
    for n in range(len(inputValues)):
        #print(currRating, inputValues[n], touchdownValues[n])

        #Case 1: Covering NEW Touchdown -> Big Plus
        if(touchdownValues[n] == 0 and inputValues[n] == 1):
            currRating += 2

        #Case 2: NEW Touchdown at 2
        if(touchdownValues[n] == 0 and inputValues[n] == 2):
            currRating += -0.25

        #Case 3: Creating Double TOuchdown
        if(touchdownValues[n] >= 1):
            currRating += -(1 + (1 * touchdownValues[n]))

    return currRating


def get_flex_sum_rating(inputMap, probecard: ProbecardClass, leastflexibleStrictMap, touchdownMap, x, y):
    #Optional Bin will always return the max Value - SiteCount

    inputValues = getMapValuesByMask(inputMap, probecard.mask_1, x, y)
    tdValues = getMapValuesByMask(touchdownMap, probecard.mask_1, x, y)
    flexValues = getMapValuesByMask(leastflexibleStrictMap, probecard.mask_1, x, y)

    score = 0
    for input, td, flex in zip(inputValues, tdValues, flexValues):
        #If one Element is Optional Touchdown OR If any touchdown occured -> Set to max (siteCount)
        if(input == 2 or td > 0):
            score += probecard.sitesCount
        #Add the LeastFlexible Options for this Die
        else:
            score += flex

        #Whatever score Evaluation (Optional etc.) Add the touchdownCount to score
        score += td
        #print(score, f"Input: {input}, td: {td}, flex: {flex}")

    return score

#Just adds the flexScore without correcting for any Empty Bins
def get_flex_sum_rating2(inputMap, probecard: ProbecardClass, leastflexibleStrictMap, touchdownMap, x, y):
    #Optional Bin will always return the max Value - SiteCount

    inputValues = getMapValuesByMask(inputMap, probecard.mask_1, x, y)
    tdValues = getMapValuesByMask(touchdownMap, probecard.mask_1, x, y)
    flexValues = getMapValuesByMask(leastflexibleStrictMap, probecard.mask_1, x, y)

    score = 0
    for input, td, flex in zip(inputValues, tdValues, flexValues):
        score += flex
        score += td

    return score

