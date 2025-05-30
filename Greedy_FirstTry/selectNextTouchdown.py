import random
import numpy as np
from Greedy_FirstTry.WaferMapClass import WaferMapClass
from Greedy_FirstTry.ProbecardClass import ProbecardClass
from Greedy_FirstTry.Touchdowns import getOnlyTouchdownByCoord
from Greedy_FirstTry.SolutionMapsClass import SolutionMapsClass


def select_next_touchdown_coords(waferMapObj: WaferMapClass, solutionMapsObj: SolutionMapsClass, probecard: ProbecardClass):
    #If there are bins where only one Touchdown is possible (Without creating double Touchdowns). Choose this Touchdown first
    leastFlexibleBins = np.argwhere(solutionMapsObj.least_flexible == 1)
    dominatingBins = np.argwhere(solutionMapsObj.dominate_Map != 0)

    #The Coordinates here show which bin has only one way to be covered. NOT the Touchdown Pos TO cover this one bin.
    #if (dominatingBins.size >= 1):
    #    maxRatingList = np.argwhere(solutionMapsObj.dominate_Map == np.max(solutionMapsObj.dominate_Map))
    #    return maxRatingList[random.randint(0, len(maxRatingList) - 1)]  # randomElement[0] == x randomElement[1] == y
    
    if (leastFlexibleBins.size >= 1):
        # Choose a random element from the list -> # randomElement[0] == x randomElement[1] == y
        randomElement = leastFlexibleBins[random.randint(0, len(leastFlexibleBins) - 1)]  
        return getOnlyTouchdownByCoord(waferMapObj.inputMap, solutionMapsObj.touchdownMap, probecard,randomElement[0], randomElement[1])

    #Get a List of all "Best" Options for next Touchdown.
    #USE ARGMAX
    maxRatingList = np.argwhere(solutionMapsObj.ratings == np.max(solutionMapsObj.ratings))
    return maxRatingList[random.randint(0, len(maxRatingList) - 1)]  # randomElement[0] == x randomElement[1] == y


#leastFlexible Strict Sum is a good way to determine a starting point.
def select_starting_touchdown_coords(waferMapObj: WaferMapClass, solutionMapsObj: SolutionMapsClass, probecard: ProbecardClass):
    minRating = np.min(solutionMapsObj.least_flexible_strict_sum)
    maxRatingList = np.argwhere(solutionMapsObj.least_flexible_strict_sum == minRating)
    randomElement = maxRatingList[random.randint(0, len(maxRatingList) - 1)]  # randomElement[0] == x randomElement[1] == y

    return randomElement