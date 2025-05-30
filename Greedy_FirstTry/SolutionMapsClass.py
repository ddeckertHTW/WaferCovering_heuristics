import copy
import numpy as np

from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE
from Greedy_FirstTry.ProbecardClass import ProbecardClass
from Greedy_FirstTry.RankingFunction import get_touchdown_rating
from Greedy_FirstTry.ShapeCoverageMinkowski import convertListToNpArray, convertListToNpArray_WithOffset, get_mask_by_coords, getMapCoordsByMask, getMapValuesByCoordList, getMapValuesByMask
from Greedy_FirstTry.PlacementOptions import getAdjacentCoordinates, get_least_flexible_map_init, getPossibleTouchdownCoordsToCoverDie, getPossibleTouchdownCoordsToCoverDie_NoDouble, getTouchdownCountForSingleDie_TdMap, \
    is_td_possible_without_double, get_least_flexible_map_init_strict, get_placement_options_count_die_strict, \
    getTouchdownCountForSingleDie_TdMap_Strict
from Greedy_FirstTry.Touchdowns import getAllFlexibleBin_Sum, rateAllPossibleTouchdowns, getAllFlexibleBin_Sum3, getAllFlexibleBin_Sum2
from Greedy_FirstTry.WaferMapClass import WaferMapClass

#TODO
class SolutionMapsClass:
    def __init__(self, inputMap, waferMapObj: WaferMapClass, probecard: ProbecardClass):
        # Main Map where all touchdowns are tracked. Used to determine leastFlexible and Rating Map
        self.touchdownMap = np.zeros_like(inputMap)

        # Log/List to save the Site1 touchdown coordinates 
        self.touchdownLocations = np.zeros_like(inputMap)
        self.touchdownLocationsList = []

        # The higher the better
        self.ratings = rateAllPossibleTouchdowns(waferMapObj) # Starting Value = IMPOSSIBLE_VALUE_NEGATIVE

        # Count of Possibilities/Options - to touch the Bin without creating a double Touchdown anywhere. 
        self.least_flexible = get_least_flexible_map_init(waferMapObj) # Starting Value = IMPOSSIBLE_VALUE_POSITIVE

        # Strict version of least_flexible_map - Not allowed ot touch Optional Bins
        self.least_flexible_strict = get_least_flexible_map_init_strict(waferMapObj) # Starting Value = 0

        # The Sum of strict LeastFlexible Bins (count of Options) per Touchdown.
        # Tells relatively how many options would be covered by a Touchdown. The Lower the Number -> The "harder"/less Options exist overall to touch all Bins in the TOuchdown 
        # ONLY USED FOR starting coords. No need to calc it later every time. 
        #self.least_flexible_strict_sum = getAllFlexibleBin_Sum2(waferMapObj, probecard, self.touchdownMap, self.least_flexible_strict)# Starting Value = IMPOSSIBLE_VALUE_POSITIVE
        self.least_flexible_strict_sum = getAllFlexibleBin_Sum(waferMapObj, probecard, self.touchdownMap, self.least_flexible_strict)# Starting Value = IMPOSSIBLE_VALUE_POSITIVE
        self.least_flexible_strict_sum2 = getAllFlexibleBin_Sum2(waferMapObj, probecard, self.touchdownMap, self.least_flexible_strict)# Starting Value = IMPOSSIBLE_VALUE_POSITIVE
        self.least_flexible_strict_sum3 = getAllFlexibleBin_Sum3(waferMapObj, probecard, self.touchdownMap, self.least_flexible_strict)# Starting Value = IMPOSSIBLE_VALUE_POSITIVE

        # Map of Touchhdowns which are directly next/adjacent to current touchdowns. So that no space would be between them. 
        # Value of Elements are the sum of leastFlexible of the Touchdown. The Lower the Number -> The "harder"/less Options exist overall to touch all Bins in the TOuchdown 
        self.td_adjacent_flex_sum = np.zeros_like(self.touchdownMap) # Starting Value = 0

        # LeastFlexible Map is empty/not Empty. Bool decides if leastFlexible calculations are skipped
        self.skip_least_flexible = np.all(self.least_flexible == 0)

        #Final Rating is calculated after solution is found.
        self.finalRating = None

        #Testing -> When leastFlexible Options are 0 on a bin. But no touchdown occured. Determine the best touchdown with minimum doubles for the bin 
        self.dominate_Map = np.zeros_like(self.touchdownMap)


    #Update PlacementOptions abd Rating here 
    def update_values_after_touchdown(self, waferMapObj: WaferMapClass, x, y):
        ###### LeastFlexible Options -> Current Touchdown Shape will not have Options without creating new Touchdowns
        td_mask = get_mask_by_coords(self.least_flexible, waferMapObj.probecard.mask_1, x, y)
        self.least_flexible[td_mask] = 0
        #self.least_flexible_strict[td_mask] = 0
        self.dominate_Map[td_mask] = 0

        ###### Log the new touchdown coords in List
        self.touchdownLocations[x][y] += 1
        self.touchdownLocationsList.append((x, y))

        # Bool if leastFlexible calculations are skipped. Once all LeastFlexible Values are 0 -> Skip everytime after 
        if(self.skip_least_flexible == False):
            self.skip_least_flexible = np.all(self.least_flexible == 0)
    

        ###### Rating Map -> Check only Touchdown Mask
        coordList_1 = getMapCoordsByMask(self.least_flexible, waferMapObj.probecard.mask_1, x, y)
        for coord in coordList_1:
            #If touchdown Not even possible -> skip
            if(waferMapObj.is_touchdown_possible_coords(coord[0],coord[1]) == False):
                continue
            
            tdValues = getMapValuesByMask(self.touchdownMap, waferMapObj.probecard.mask_1, coord[0],coord[1])
            inputMapValues = getMapValuesByMask(waferMapObj.inputMap, waferMapObj.probecard.mask_1, coord[0],coord[1])

            self.ratings[coord[0]][coord[1]] = get_touchdown_rating(inputMapValues, tdValues)


        ###### Rating Map AND LeastFlexible Map -> Check Outer Ring (Cover5)
        coordList_5 = getMapCoordsByMask(self.least_flexible, waferMapObj.probecard.mask_5, x, y)
        for coord in coordList_5:
            #Rating Map
            if(waferMapObj.is_touchdown_possible_coords(coord[0],coord[1]) == True):
                tdValues = getMapValuesByMask(self.touchdownMap, waferMapObj.probecard.mask_1, coord[0],coord[1])
                inputMapValues = getMapValuesByMask(waferMapObj.inputMap, waferMapObj.probecard.mask_1, coord[0],coord[1])

                self.ratings[coord[0]][coord[1]] = get_touchdown_rating(inputMapValues, tdValues)
                #Is that reset correct? When rating changes adjacent to one bin yes.?
                self.td_adjacent_flex_sum[coord[0]][coord[1]] = 0
                #if(self.td_adjacent_flex_sum[coord[0]][coord[1]] > 0 and self.ratings[coord[0]][coord[1]] != IMPOSSIBLE_VALUE_NEGATIVE):
                #    self.ratings[coord[0]][coord[1]] = self.ratings[coord[0]][coord[1]] + (1 / self.td_adjacent_flex_sum[coord[0]][coord[1]]) * 100
            
            #Least Flexible 
            if(self.skip_least_flexible == False and waferMapObj.is_touchdown_possible_and_mandatory_coords(coord[0],coord[1]) == True):
                prevValue = self.least_flexible[coord[0]][coord[1]]

                self.least_flexible[coord[0]][coord[1]] = getTouchdownCountForSingleDie_TdMap(waferMapObj, coord[0], coord[1], self.touchdownMap)
                #self.least_flexible_strict[coord[0]][coord[1]] = getTouchdownCountForSingleDie_TdMap_Strict(waferMapObj, coord[0], coord[1], self.touchdownMap, waferMapObj.inputMap)


                # DOMINANZ -> Look at all possible Touchdowns per Die 
                # FInd Bins that are now least_flexible == 0 but before this round were not 0. -> they were not covered by a touchdown but have no least Flexible
                if(prevValue != 0 and self.least_flexible[coord[0]][coord[1]] == 0):     
                    #Get all coords that can cover the current die and find the max 
                    possibleCoords = getPossibleTouchdownCoordsToCoverDie(waferMapObj, coord[0], coord[1])               
                    values = getMapValuesByCoordList(self.ratings, possibleCoords)
                    #Looop over every value that has the amx Value
                    for currIndex in [index for index, value in enumerate(values) if value == max(values)]:
                        self.dominate_Map[possibleCoords[currIndex][0]][possibleCoords[currIndex][1]] = self.ratings[possibleCoords[currIndex][0]][possibleCoords[currIndex][1]]


        #adjacent least Flexible can be skipped if no leastFlexible remaining
        if(self.skip_least_flexible):
            return

        ###### td_adjacent_flex_sum Touchdown Adjacent Sum Map -> Loop over adjacent Mask and if touchdown possible without double - Sum of least Flexuble Map on that Die 
        coordList_adjacent = getMapCoordsByMask(self.least_flexible, waferMapObj.probecard.mask_adjacent, x, y)
        for coord in coordList_adjacent:
            if(is_td_possible_without_double(waferMapObj, coord[0], coord[1], self.touchdownMap)):
                self.td_adjacent_flex_sum[coord[0]][coord[1]] = sum(getMapValuesByMask(self.least_flexible, waferMapObj.probecard.mask_1, coord[0],coord[1]))
                self.ratings[coord[0]][coord[1]] = self.ratings[coord[0]][coord[1]] + (1 / self.td_adjacent_flex_sum[coord[0]][coord[1]]) * 100
            else:
                self.td_adjacent_flex_sum[coord[0]][coord[1]] = 0

        return
        print()


    def update_weighted_descicion_values(self,):
        #Alle Maps in 1/2 Maps mit gewichtung verwandeln
        taoksnd = False