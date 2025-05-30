from typing import Tuple
import numpy as np
from Greedy_Optimized.HelperFunc.print_colored_debug_maps import print_colored_TD_leastFlex_score
from Greedy_Optimized.Probecard.getProbecardByName import getProbecardByName
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass
from Greedy_Optimized.Solution.update_decision_variables import update_decision_variables_init


#LOADING EXISTING TOUCHDOWNS !!!???? HOW

## Initializes WaferMap object & SolutionClass object
def init_greedy_data(inputMapFilepath, probecardSize, td_scenario_list = None, weightSettingsObj:WeightSettingsClass = None) -> Tuple[WaferMapClass, SolutionMapClass]:
    #Load InputMap
    inputMap =  np.loadtxt(inputMapFilepath, dtype=int)  #2D np Array of InputMap

    #Load Probecard
    probecard = getProbecardByName(probecardSize)

    # The Object with fixed Values like inputMap/Probecard. Does not need deep Copy because no Values are changing
    waferMapObj = WaferMapClass(inputMap, probecard, td_scenario_list, weightSettingsObj)

    #The Object with the "changing" Evaluation Values. For each Solution all relevant decision variables are stored here
    solutionObj = SolutionMapClass(waferMapObj)

    # Update the 2 decision Maps To be able to place the first Touchdown.
    update_decision_variables_init(waferMapObj, solutionObj)

    #solutionObj.printScoreNpArray()
    #solutionObj.printLeastFlexNpArray()
    #solutionObj.printLeastFlexStrictNpArray()
    #solutionObj.printLeastFlexStrictSUMNpArray(

    return waferMapObj, solutionObj
