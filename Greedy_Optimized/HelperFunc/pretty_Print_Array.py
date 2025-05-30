import copy
import numpy as np
from colorama import Fore, Style, init

from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE
from Greedy_FirstTry.ProbecardClass import ProbecardClass
from Greedy_FirstTry.ShapeCoverageMinkowski import convertListToNpArray_WithOffset, getMapCoordsByMask
from Greedy_FirstTry.SolutionMapsClass import SolutionMapsClass
from Greedy_FirstTry.Touchdowns import placeTouchdownOnPos
from Greedy_FirstTry.WaferMapClass import WaferMapClass


COLOR_CURR_TOUCHDOWN = Fore.RED
COLOR_TOUCHDOWNs = Fore.BLUE
COLOR_UPDATE = Fore.CYAN

COLOR_MANDATORY = Fore.LIGHTGREEN_EX
COLOR_OPTIONAL = Fore.LIGHTYELLOW_EX
COLOR_FORBIDDEN = Fore.WHITE

COLOR_HIGHLIGHT = Fore.LIGHTYELLOW_EX
COLOR_COORDSYSTEM = Fore.RED

def prettyPrintArray(matrixToPrint,localString = ""):
    print(localString,"\n",np.array2string(matrixToPrint, suppress_small=True, formatter={'float': '{:0.4f}'.format})[1:-1])


def printArrayParallel_2(array1, array2, message):
    printString = ""
    for x in range(array1.shape[0]):
        for y in range(array1.shape[1]):
            printString += f"{array1[x][y]} "

        printString += "\t"
        for y in range(array2.shape[1]):
            printString += f"{array2[x][y]} "

        printString += "\n"

    print(f"{message}: \n{printString}")


def printArrayParallel_3(array1, array2, array3, message):
    printString = ""
    for x in range(array1.shape[0]):
        for y in range(array1.shape[1]):
            printString += f"{array1[x][y]} "

        printString += "\t"
        for y in range(array2.shape[1]):
            printString += f"{array2[x][y]} "

        printString += "\t"
        for y in range(array3.shape[1]):
            printString += f"{array3[x][y]} "

        printString += "\n"

    print(f"{message}: \n{printString}")

#def printArrayParallel_3_Color(message, touchdownMap, leastFlexibleMap, ratingMap, probecard: ProbecardClass, x, y):
def printArrayParallel_3_Color(message, map1, map2, map3, probecard: ProbecardClass, td_x, td_y):
    def getValueOrPlaceholder(value):
        if(value == IMPOSSIBLE_VALUE_NEGATIVE or value == IMPOSSIBLE_VALUE_POSITIVE or value == None):
            return placeholder
        return value
    
    printString = ""
    element_width = 3
    placeholder = "-"

    color1 = COLOR_CURR_TOUCHDOWN
    color2 = COLOR_UPDATE

    touchdownCoords = getMapCoordsByMask(map1, probecard.mask_1, td_x, td_y)
    leastFlexibleMapCoords = getMapCoordsByMask(map2, probecard.mask_3, td_x, td_y)

    for td_x in range(map1.shape[0]):
        for td_y in range(map1.shape[1]):
            element_width = 1
            #printString += f"{touchdownMap[x][y]} "
            if (td_x, td_y) in touchdownCoords:
                printString += f"{color1}{getValueOrPlaceholder(map1[td_x][td_y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(map1[td_x][td_y]):^{element_width}} "


        element_width = 2
        printString += "\t"
        for td_y in range(map2.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if (np.all(map2 == 0)):
                printString += f"{getValueOrPlaceholder(map2[td_x][td_y]):^{element_width}} "
            # Color the Inside Probecard Shape
            elif (td_x, td_y) in touchdownCoords:
                printString += f"{color1}{getValueOrPlaceholder(map2[td_x][td_y]):^{element_width}}{Style.RESET_ALL} "
            # COlor the cover 3 - Range where we update
            elif (td_x, td_y) in leastFlexibleMapCoords:
                printString += f"{color2}{getValueOrPlaceholder(map2[td_x][td_y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(map2[td_x][td_y]):^{element_width}} "

        element_width = 3
        printString += "\t"
        for td_y in range(map3.shape[1]):
            #printString += f"{ratingMap[x][y]} "
            if (td_x, td_y) in leastFlexibleMapCoords:
                printString += f"{color1}{getValueOrPlaceholder(map3[td_x][td_y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(map3[td_x][td_y]):^{element_width}}{Style.RESET_ALL} "
        
        printString += "\n"

    print(f"{message}: \n{printString}", end='')

def printArray_Color_Td_Flex_Rating(solutionMapsObj: SolutionMapsClass, waferMapObj: WaferMapClass, probecard: ProbecardClass, td_x, td_y):
    
    def getValueOrPlaceholder(value):
        if(value == IMPOSSIBLE_VALUE_NEGATIVE or value == IMPOSSIBLE_VALUE_POSITIVE or value == None):
            return placeholder
        return value
    
    printString = ""
    element_width = 3
    placeholder = "-"
    message = "Touchdowns (Green:MUST) \tLeastFlexible (Yellow = Forced) \tRatings (Yellow = Adjacent To Touchdown -> Boost)"

    touchdown_mask_coords = getMapCoordsByMask(waferMapObj.inputMap, probecard.mask_1, td_x, td_y)
    update_mask_coords = getMapCoordsByMask(waferMapObj.inputMap, probecard.mask_3, td_x, td_y)

    map1 = solutionMapsObj.touchdownMap
    map2 = solutionMapsObj.least_flexible
    map3 = solutionMapsObj.ratings

    maxRating = np.max(map3)

    #Y Coords on Top
    printString += f"{COLOR_COORDSYSTEM}"
    for y in range(map1.shape[1]):
        printString += f"{y%10} "
    printString += "\t"

    for y in range(map2.shape[1]):
        printString += f"{y%10} "
    printString += "\t"
  
    for y in range(map3.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):

        #TouchdownMap with Mandatory/Optional Highlighing
        for y in range(map1.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{map1[x][y]}{Style.RESET_ALL} "
            #Inputmap COloring 
            elif (solutionMapsObj.touchdownMap[x][y] >= 1):
                printString += f"{COLOR_TOUCHDOWNs}{map1[x][y]}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 1):
                printString += f"{COLOR_MANDATORY}{map1[x][y]}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 2):
                printString += f"{COLOR_OPTIONAL}{map1[x][y]}{Style.RESET_ALL} "
            else:
                printString += f"{map1[x][y]} "

        #LEAST FLEXIBLE MAP
        printString += "\t"
        for y in range(map2.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if (np.all(map2 == 0)):
                printString += f"{map2[x][y]} "
            #Touchdown Shape
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{map2[x][y]}{Style.RESET_ALL} "
            #If least Flexible == 1 -> Will be mandatory
            elif (map2[x][y] == 1):
                printString += f"{COLOR_HIGHLIGHT}{map2[x][y]}{Style.RESET_ALL} "
            #Update Shape
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{map2[x][y]}{Style.RESET_ALL} "
            elif (map2[x][y] == 0):
                printString += f"{COLOR_FORBIDDEN}{map2[x][y]}{Style.RESET_ALL} "
            else:
                printString += f"{map2[x][y]} "


        printString += "\t"
        for y in range(map3.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(map3[x][y]):^{element_width}}{Style.RESET_ALL} "
            #Highlight the best Element
            #elif(map3[x][y] == maxRating):
            elif (solutionMapsObj.td_adjacent_flex_sum[x][y] >= 1):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(map3[x][y]):^{element_width}}{Style.RESET_ALL} "
            #Update Shape
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{getValueOrPlaceholder(map3[x][y]):^{element_width}}{Style.RESET_ALL} "
            elif(getValueOrPlaceholder(map3[x][y]) == placeholder):
                printString += f"{COLOR_FORBIDDEN}{getValueOrPlaceholder(map3[x][y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(map3[x][y]):^{element_width}} "

        
        printString += "\n"

    print(f"{message}: \n{printString}", end='')

def printArray_Color_Domninaz_Adjacent_FlexSum(solutionMapsObj: SolutionMapsClass, waferMapObj: WaferMapClass, probecard: ProbecardClass, x, y):
    
    def getValueOrPlaceholder(value):
        if(value == IMPOSSIBLE_VALUE_NEGATIVE or value == IMPOSSIBLE_VALUE_POSITIVE or value == None):
            return placeholder
        return value
    
    printString = ""
    element_width = 2
    placeholder = "-"
    message = "Dominanz (Red:MUST) \t\tAdjacent (Yellow = Rating Buff) \tFlexSum (Static)"

    touchdown_mask_coords = getMapCoordsByMask(waferMapObj.inputMap, probecard.mask_1, x, y)
    update_mask_coords = getMapCoordsByMask(waferMapObj.inputMap, probecard.mask_3, x, y)
    adjacent_mask_coords = getMapCoordsByMask(waferMapObj.inputMap, probecard.mask_adjacent, x, y)

    map1 = solutionMapsObj.dominate_Map
    map2 = solutionMapsObj.td_adjacent_flex_sum
    map3 = solutionMapsObj.dominate_Map

    maxRating = np.max(map3)
    printString += f"{COLOR_COORDSYSTEM}"
    #Y Coords on Top
    for y in range(map1.shape[1]):
        printString += f"{y%10} "
    printString += "\t"

    for y in range(map2.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += "\t"
  
    for y in range(map3.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):
        #Dominate Map
        for y in range(map1.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if(solutionMapsObj.dominate_Map[x][y] >= 1):
                printString += f"{COLOR_CURR_TOUCHDOWN}{map1[x][y]}{Style.RESET_ALL} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{map1[x][y]}{Style.RESET_ALL} "
            elif (solutionMapsObj.touchdownMap[x][y] >= 1):
                printString += f"{COLOR_TOUCHDOWNs}{map1[x][y]}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 1):
                printString += f"{COLOR_MANDATORY}{map1[x][y]}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 2):
                printString += f"{COLOR_OPTIONAL}{map1[x][y]}{Style.RESET_ALL} "

            else:
                printString += f"{COLOR_FORBIDDEN}{map1[x][y]}{Style.RESET_ALL} "


        element_width = 2
        #td_adjacent_flex_sum Map
        printString += "\t"
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (np.all(map2 == 0)):
                printString += f"{map2[x][y]:^{element_width}} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{map2[x][y]:^{element_width}}{Style.RESET_ALL} "
                #If any Value is written -> Highlight
            elif (solutionMapsObj.td_adjacent_flex_sum[x][y] >= 1):
                printString += f"{COLOR_HIGHLIGHT}{map2[x][y]:^{element_width}}{Style.RESET_ALL} "
            #Adjacent Mask
            elif (x, y) in adjacent_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{map2[x][y]:^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{map2[x][y]:^{element_width}} "

        printString += "\t"
        for y in range(map3.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(map3[x][y]):^{element_width}}{Style.RESET_ALL} "
            #Update Shape
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{getValueOrPlaceholder(map3[x][y]):^{element_width}}{Style.RESET_ALL} "
            elif(getValueOrPlaceholder(map3[x][y]) == placeholder):
                printString += f"{COLOR_FORBIDDEN}{getValueOrPlaceholder(map3[x][y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(map3[x][y]):^{element_width}} "

        
        printString += "\n"

    print(f"{message}: \n{printString}", end='')


def printSolutionMapObj_timeline(touchdownLocationsList, solutionMapsObj_init: SolutionMapsClass, waferMapObj: WaferMapClass):
    #return None
    solutionMapsObj = copy.deepcopy(solutionMapsObj_init)

    #Replicate all calculations of element
    for tdCoords in touchdownLocationsList:
            
        placeTouchdownOnPos(waferMapObj.inputMap, solutionMapsObj.touchdownMap, waferMapObj.probecard, tdCoords[0], tdCoords[1])
        solutionMapsObj.update_values_after_touchdown(waferMapObj, tdCoords[0], tdCoords[1])

        printArrayParallel_3_Color("Touchdowns, LeastFlexible, Rating - Map. Count: ", solutionMapsObj.touchdownMap, 
                                   solutionMapsObj.least_flexible, solutionMapsObj.ratings, waferMapObj.probecard, tdCoords[0], tdCoords[1])        

"""
        from HelperFunc.pretty_Print_Array import printMaskOfMap
        printMaskOfMap(waferMapObj, x, y , self.touchdownMap)

"""
def printMaskOfMap(waferMapObj: WaferMapClass, x, y, map):
    #Only the Mask... Not the Value of the Map
    #print(convertListToNpArray(getMapCoordsByMask(self.touchdownMap,waferMapObj.probecard.mask_5, x, y )))
        
    newArr, x_Offset, y_Offset = convertListToNpArray_WithOffset(getMapCoordsByMask(map,waferMapObj.probecard.mask_5, x, y ))
    test = map[x_Offset: x_Offset + newArr.shape[0], y_Offset: y_Offset + newArr.shape[1]]
    print(test)
