import datetime

import numpy as np
from Greedy_Optimized.HelperFunc.print_colored_debug_maps import print_colored_PrevTdMaps, print_colored_Rating_Maps, print_colored_TD_leastFlex_score, print_colored_decision_maps, print_colored_dominanz_adjacent_flexSum, print_colored_static_maps
from Greedy_Optimized.Solution.ResultClass import ResultClass
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Solution.remove_redundant_TDs import remove_redundant_TDs
from Greedy_Optimized.Solution.update_decision_variables import update_decision_variables
from Greedy_Optimized.Solution.update_values_after_touchdown import update_values_after_touchdown
from Greedy_Optimized.Touchdown.place_touchdown import place_touchdown
from Greedy_Optimized.Touchdown.select_next_touchdown import select_next_touchdown

## This function is the main internal loop for one greedy run
#  best touchdowns are chosen and placed, then solution object is updated
def Greedy_Loop(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, init_time_total: datetime.timedelta, debugPrint = False, max_loop_count = 15900):
    loop_start_time = datetime.datetime.now()

    if debugPrint:
        print_colored_TD_leastFlex_score(0, 0, waferMapObj, solutionObj)
        print_colored_dominanz_adjacent_flexSum(0, 0, waferMapObj, solutionObj)
        print_colored_decision_maps(0, 0, waferMapObj, solutionObj.ratings_map, solutionObj.forced_leastFlex_map)
        print()

    for loopCount in range(max_loop_count):
        #Break out of loop when solution is found and return the Solution found
        if(solutionObj.check_if_solved()):
            #Check for optimizaion
            removed_redundant_Tds = remove_redundant_TDs(waferMapObj, solutionObj, debugPrint)
            return ResultClass(solutionObj, waferMapObj.inputMap,init_time_total, loop_start_time, redundant_Tds = removed_redundant_Tds)
        
        td_x, td_y = select_next_touchdown(solutionObj, waferMapObj)

        #In Case of Error with Touchdown Placement. Return None
        if td_x is None or td_y is None:
            return None 

        # Load coords from fixed scenario List, if given
        #if(td_scenario_list is not None and loopCount in td_scenario_list): td_x, td_y = td_scenario_list[loopCount] #Dictionary like: {0: (4,4), 1:(5,5), 2:(6,6)}
        if(waferMapObj.td_scenario_list is not None and loopCount < len(waferMapObj.td_scenario_list)): td_x, td_y = waferMapObj.td_scenario_list[loopCount] # Array like:  [ [9, 9], [11, 8],[10, 6]]

        # Place selected Touchdown
        place_touchdown(td_x, td_y, waferMapObj, solutionObj)
        
        # Update solutionObj after placed TD
        update_values_after_touchdown(td_x, td_y, waferMapObj, solutionObj)

        update_decision_variables(td_x, td_y, waferMapObj, solutionObj)
        
        if debugPrint: 
            #print_colored_TD_leastFlex_score(td_x, td_y, waferMapObj, solutionObj)
            #print_colored_Rating_Maps(td_x, td_y, waferMapObj, solutionObj, solutionObj.ratings_map)

            print_colored_dominanz_adjacent_flexSum(td_x, td_y, waferMapObj, solutionObj)
            print_colored_static_maps(td_x, td_y, waferMapObj, solutionObj)

            #print_colored_PrevTdMaps(td_x, td_y, waferMapObj, solutionObj)
            print_colored_TD_leastFlex_score(td_x, td_y, waferMapObj, solutionObj)#
            print_colored_decision_maps(td_x, td_y, waferMapObj, solutionObj.ratings_map, solutionObj.forced_leastFlex_map)

            print(" ######################################################################## ")

    if (debugPrint): print(f"[MAX LOOP COUNT REACHED: ({max_loop_count})] - TERMINATING RUN\n")
    return None
