from colorama import Fore, Style
import numpy as np
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE
from Greedy_Optimized.NPMaskOperations.get_coordinates_by_mask import get_coordinates_by_mask
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

COLOR_CURR_TOUCHDOWN = Fore.RED
COLOR_TOUCHDOWNs = Fore.BLUE
COLOR_UPDATE = Fore.CYAN

COLOR_MANDATORY = Fore.LIGHTGREEN_EX
COLOR_OPTIONAL = Fore.LIGHTYELLOW_EX
COLOR_FORBIDDEN = Fore.WHITE

COLOR_HIGHLIGHT = Fore.LIGHTYELLOW_EX
COLOR_COORDSYSTEM = Fore.RED

placeholder = "-"

def getValueOrPlaceholder(value):
    if(value == IMPOSSIBLE_VALUE_NEGATIVE or value == IMPOSSIBLE_VALUE_POSITIVE or value == None):
        return placeholder
    return int(value)

def getValueOrPlaceholder_Rounded(value):
    if(value == IMPOSSIBLE_VALUE_NEGATIVE or value == IMPOSSIBLE_VALUE_POSITIVE or value == None):
        return placeholder
    return round(value, 1)

def print_two_arrays(array1, array2):
    printString = ""
    message = "Yellow Highlight is the MAX elements"
    element_width = 3

    array1_max = np.max(array1)
    array2_max = np.max(array2)


    printString += f"{COLOR_COORDSYSTEM}"
    #Y Coords on Top
    for y in range(array1.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += "\t"

    for y in range(array2.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(array1.shape[0]):
        #RATING MAP
        for y in range(array1.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if(array1[x][y] == array1_max):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(array1[x][y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(array1[x][y]):^{element_width}} "

        #forced_options_map
        printString += "\t"
        for y in range(array2.shape[1]):
            if(array2[x][y] == array2_max):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(array2[x][y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(array2[x][y]):^{element_width}} "

        printString += "\n"

    print(f"{message}: \n{printString}", end='')


def print_colored_TD_leastFlex_score(td_x, td_y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):    
    printString = ""
    message = "Touchdowns (Green:MUST) \tLeastFlexible (Yellow = Forced) \score_gain (Yellow = Adjacent To Touchdown -> Boost)"
    element_width = 3

    touchdown_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_1)
    update_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_3)

    #Y Coords on Top
    printString += f"{COLOR_COORDSYSTEM}"
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10} "
    printString += "\t"

    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10} "
    printString += "\t"
  
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):

        #TouchdownMap with Mandatory/Optional Highlighing
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown)}{Style.RESET_ALL} "
            #Inputmap COloring 
            elif (solutionObj.dieMap[x][y].touchdown >= 1):
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 1):
                printString += f"{COLOR_MANDATORY}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 2):
                printString += f"{COLOR_OPTIONAL}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown)}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown)} "

        #LEAST FLEXIBLE MAP
        printString += "\t"
        for y in range(waferMapObj.inputMap.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            
            if (all(die.least_flexible == 0 for row in solutionObj.dieMap for die in row)):
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].least_flexible)} "
            #Touchdown Shape
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].least_flexible)}{Style.RESET_ALL} "
            #If least Flexible == 1 -> Will be mandatory
            elif (solutionObj.dieMap[x][y].least_flexible == 1):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(solutionObj.dieMap[x][y].least_flexible)}{Style.RESET_ALL} "
            #Update Shape
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{getValueOrPlaceholder(solutionObj.dieMap[x][y].least_flexible)}{Style.RESET_ALL} "
            elif (solutionObj.dieMap[x][y].least_flexible == 0):
                printString += f"{COLOR_FORBIDDEN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].least_flexible)}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].least_flexible)} "


        printString += "\t"
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].score_gain):^{element_width}}{Style.RESET_ALL} "
            #Highlight the best Element
            #elif(solutionObj.dieMap[x][y].score_gain == maxRating):
            elif (solutionObj.dieMap[x][y].adjacent_flex_sum >= 1 and getValueOrPlaceholder(solutionObj.dieMap[x][y].forbidden_distance_static) != placeholder):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(solutionObj.dieMap[x][y].score_gain):^{element_width}}{Style.RESET_ALL} "
            #Update Shape
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{getValueOrPlaceholder(solutionObj.dieMap[x][y].score_gain):^{element_width}}{Style.RESET_ALL} "
            elif(getValueOrPlaceholder(solutionObj.dieMap[x][y].score_gain) == placeholder):
                printString += f"{COLOR_FORBIDDEN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].score_gain):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].score_gain):^{element_width}} "

        
        printString += "\n"

    print(f"{message}: \n{printString}", end='')

def print_colored_dominanz_adjacent_flexSum(td_x, td_y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):        
    printString = ""
    message = "dominate (Red:MUST) \tadjacent_flex_sum (Yellow = Rating Buff) forbidden_distance_static (Static)"
    element_width = 2

    touchdown_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_1)
    update_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_3)
    adjacent_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_adjacent)


    printString += f"{COLOR_COORDSYSTEM}"
    #Y Coords on Top
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10} "
    printString += "\t"

    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += "\t"
  
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):
        #Dominate Map
        for y in range(waferMapObj.inputMap.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if(solutionObj.dieMap[x][y].dominate >= 1):
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].dominate)}{Style.RESET_ALL} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].dominate)}{Style.RESET_ALL} "
            elif (solutionObj.dieMap[x][y].touchdown >= 1):
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].dominate)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 1):
                printString += f"{COLOR_MANDATORY}{getValueOrPlaceholder(solutionObj.dieMap[x][y].dominate)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 2):
                printString += f"{COLOR_OPTIONAL}{getValueOrPlaceholder(solutionObj.dieMap[x][y].dominate)}{Style.RESET_ALL} "

            else:
                printString += f"{COLOR_FORBIDDEN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].dominate)}{Style.RESET_ALL} "


        #td_adjacent_flex_sum Map
        printString += "\t"
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (all(die.adjacent_flex_sum == 0 for row in solutionObj.dieMap for die in row)):
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "
            #If any Value is written -> Highlight
            elif (solutionObj.dieMap[x][y].adjacent_flex_sum >= 1):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "
            #Adjacent Mask
            elif (x, y) in adjacent_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "
                        #Update Area
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "

            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}} "

        printString += "\t"
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].forbidden_distance_static):^{element_width}}{Style.RESET_ALL} "
            #Update Shape
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{getValueOrPlaceholder(solutionObj.dieMap[x][y].forbidden_distance_static):^{element_width}}{Style.RESET_ALL} "
            elif(getValueOrPlaceholder(solutionObj.dieMap[x][y].forbidden_distance_static) == placeholder):
                printString += f"{COLOR_FORBIDDEN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].forbidden_distance_static):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].forbidden_distance_static):^{element_width}} "

        
        printString += "\n"

    print(f"{message}: \n{printString}", end='')


def print_colored_decision_maps(td_x, td_y, waferMapObj: WaferMapClass, ratings_map, forced_options_map):
    printString = ""
    message = "Ratings Map (Yellow = Highest Value) \t\t\t\t Forced Options (Yellow = Highest Value) "
    element_width = 3

    touchdown_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_1)

    rating_max = np.max(ratings_map)
    forced_max = np.max(forced_options_map)


    printString += f"{COLOR_COORDSYSTEM}"
    #Y Coords on Top
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += "\t"

    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):
        #RATING MAP
        for y in range(waferMapObj.inputMap.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if(ratings_map[x][y] == rating_max):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder_Rounded(ratings_map[x][y]):^{element_width}}{Style.RESET_ALL} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder_Rounded(ratings_map[x][y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder_Rounded(ratings_map[x][y]):^{element_width}} "

        #forced_options_map
        printString += "\t"
        for y in range(waferMapObj.inputMap.shape[1]):
            if(forced_options_map[x][y] == forced_max and forced_options_map[x][y] != 0):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(forced_options_map[x][y]):^{element_width}}{Style.RESET_ALL} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(forced_options_map[x][y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(forced_options_map[x][y]):^{element_width}} "

        printString += "\n"

    print(f"{message}: \n{printString}", end='')

def print_colored_PrevTdMaps(td_x, td_y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):    
    printString = ""
    message = "Prev TD Rating Map \t\t\t PrevTD Map \t\t\t\tPrev + Current TD Map in one"
    element_width = 3

    touchdown_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_1)
    update_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_3)

    #Y Coords on Top
    printString += f"{COLOR_COORDSYSTEM}"
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10} "
    printString += "\t"

    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10} "
    printString += "\t"
  
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):
        #TOUCHDOWN
      
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_score_gain)}{Style.RESET_ALL} "
            #Inputmap COloring 
            elif (solutionObj.dieMap[x][y].prev_td_score_gain >= 1):
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_score_gain)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 1):
                printString += f"{COLOR_MANDATORY}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_score_gain)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 2):
                printString += f"{COLOR_OPTIONAL}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_score_gain)}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_score_gain)} "


        printString += "\t"
        #TouchdownMap with Mandatory/Optional Highlighing
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            #Inputmap COloring 
            elif (solutionObj.dieMap[x][y].prev_td_count >= 1):
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 1):
                printString += f"{COLOR_MANDATORY}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 2):
                printString += f"{COLOR_OPTIONAL}{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].prev_td_count)} "
        
        printString += "\t"
        #TouchdownMap with Mandatory/Optional Highlighing
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown + solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            #Inputmap COloring 
            elif (solutionObj.dieMap[x][y].touchdown >= 1):
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown + solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 1):
                printString += f"{COLOR_MANDATORY}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown + solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            elif (waferMapObj.inputMap[x][y] == 2):
                printString += f"{COLOR_OPTIONAL}{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown + solutionObj.dieMap[x][y].prev_td_count)}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].touchdown + solutionObj.dieMap[x][y].prev_td_count)} "
        
        printString += "\n"

    print(f"{message}: \n{printString}", end='')


def print_colored_Rating_Maps(td_x, td_y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, ratings_map):    
    printString = ""
    message = "\tRating Decision (Yellow = Best) \tAdjacent TDs (Yellow = Adjacent To Touchdown -> Boost) \tScore ()"
    element_width = 3

    touchdown_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_1)
    update_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_3)
    adjacent_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_adjacent)

    rating_max = np.max(ratings_map)

    #Y Coords on Top
    printString += f"{COLOR_COORDSYSTEM}"
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += "\t"

    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10} "
    printString += "\t"
    
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):        
        #RATING MAP
        for y in range(waferMapObj.inputMap.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if(ratings_map[x][y] == rating_max):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(ratings_map[x][y]):^{element_width}}{Style.RESET_ALL} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(ratings_map[x][y]):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(ratings_map[x][y]):^{element_width}} "

       
        for y in range(waferMapObj.inputMap.shape[1]):
            #Touchdown Shape
            if (all(die.adjacent_flex_sum == 0 for row in solutionObj.dieMap for die in row)):
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_CURR_TOUCHDOWN}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "
            #If any Value is written -> Highlight
            elif (solutionObj.dieMap[x][y].adjacent_flex_sum >= 1):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "
            #Adjacent Mask
            elif (x, y) in adjacent_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "
                        #Update Area
            elif (x, y) in update_mask_coords:
                printString += f"{COLOR_UPDATE}{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}}{Style.RESET_ALL} "

            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].adjacent_flex_sum):^{element_width}} "

        
        printString += "\n"

    print(f"{message}: \n{printString}", end='')



def print_colored_static_maps(td_x, td_y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass):
    printString = ""
    message = "Optional Count \t\t\t\t Distance to Mandatory "
    element_width = 3

    touchdown_mask_coords = get_coordinates_by_mask(td_x, td_y, waferMapObj.inputMap, waferMapObj.probecard.mask_1)

    Optional_max = waferMapObj.probecard.sitesCount
    Distance_max = 1


    printString += f"{COLOR_COORDSYSTEM}"
    #Y Coords on Top
    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += "\t"

    for y in range(waferMapObj.inputMap.shape[1]):
        printString += f"{y%10:^{element_width}} "
    printString += f"{Style.RESET_ALL}\n"

    for x in range(waferMapObj.inputMap.shape[0]):
        #RATING MAP
        for y in range(waferMapObj.inputMap.shape[1]):
            #If everything is 0 -> No need for coloring anymore
            if(solutionObj.dieMap[x][y].optional_covered_buff_static == Optional_max):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder(solutionObj.dieMap[x][y].optional_covered_buff_static):^{element_width}}{Style.RESET_ALL} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder(solutionObj.dieMap[x][y].optional_covered_buff_static):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder(solutionObj.dieMap[x][y].optional_covered_buff_static):^{element_width}} "

        #forced_options_map
        printString += "\t"
        for y in range(waferMapObj.inputMap.shape[1]):
            if(solutionObj.dieMap[x][y].forbidden_distance_static == Distance_max):
                printString += f"{COLOR_HIGHLIGHT}{getValueOrPlaceholder_Rounded(solutionObj.dieMap[x][y].forbidden_distance_static):^{element_width}}{Style.RESET_ALL} "
            elif (x, y) in touchdown_mask_coords:
                printString += f"{COLOR_TOUCHDOWNs}{getValueOrPlaceholder_Rounded(solutionObj.dieMap[x][y].forbidden_distance_static):^{element_width}}{Style.RESET_ALL} "
            else:
                printString += f"{getValueOrPlaceholder_Rounded(solutionObj.dieMap[x][y].forbidden_distance_static):^{element_width}} "

        printString += "\n"

    print(f"{message}: \n{printString}", end='')
