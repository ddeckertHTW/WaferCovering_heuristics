# To avoid incrementing the touchdown Map every time. "Atrificially" add 1 to the TouchdownMap Values
from typing import List
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, PENALTY_SCORE, InputMapStatus_FORBIDDEN, InputMapStatus_MANDATORY, InputMapStatus_OPTIONAL
from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

#MAGIC NUMBERS??? HOW AND WHERE TO DEFINE

# +1 Point for Newly covered Bin. -n for every n-th double Touchwon (-1,-2 for the 2. and 3. Touchdown)#
# And a small -0.1 for every Optional Bin that is covered. So that two equal Touchdowns scores have a debuff if "noting new" is covered.  
def get_td_score_gain(x, y, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass) -> int:
    # Score for Die makes no sense if Touchdown is not even legal...
    if(solutionObj.dieMap[x][y].td_possible_as_site1 == False):
        return IMPOSSIBLE_VALUE_NEGATIVE
    
    #Get all touchdown dies, to evaluate them
    td_Dies: List[DieClass] = get_values_by_mask(x,y, solutionObj.dieMap, waferMapObj.probecard.mask_1)
    return get_td_score_gain_by_List(td_Dies)


# Zielfunktion: 2^n. Scale must be adjusted, so that the Optional Die is exactly at 0. Which is the middle of Touchdown 1 and 2 
# Touchdown 1:2, 2:4, 3:8, 4:16
# Adjusted Scale: 1:2, 2:-2, 3: -6, 4:-14


# SolutionMap Init does not need to calculate this again
def get_td_score_gain_by_List(td_Dies: List[DieClass]) -> int:
    #There needs to be atleast 1 Must touch die, that is not allready touched. If not return IMPOSSIBLE_VALUE_NEGATIVE
    new_mandatory_td_Flag = False

    currRating = 0
    for die in td_Dies: #Loop over all Dies that the x/y Coords as Site 1 would touch and create the score
        #If ANY Element of this touchdown has a 0 on InputMap -> NOT ALLOWED
        if(die.inputMap_value == InputMapStatus_FORBIDDEN): #InputMapStatus.FORBIDDEN.value
            return IMPOSSIBLE_VALUE_NEGATIVE

        #Case 1: NEW Touchdown on Mandatory Die -> Big Reward
        if(die.touchdown == 0 and die.inputMap_value == InputMapStatus_MANDATORY): #InputMapStatus.MANDATORY.value
            currRating += PENALTY_SCORE #2^1 == 2

        #Case 2: Creating a double Touchdown on a Mandtory Die 
        # -> Big Punishment. (Must be larger than Gain from new Touchdown)
        if(die.touchdown >= 1 and die.inputMap_value == InputMapStatus_MANDATORY): #InputMapStatus.MANDATORY.value
            currRating += -pow(PENALTY_SCORE, die.touchdown)
            #currRating += -(0.5 + 1 * die.touchdown) #Magic Numbers is bad


        #Case 3: NEW OR Double Touchdown on a Optional Die 
        # -> Small Negative, to avoid a TIE with a Touchdown that covers Mandatory Dies with double TDs
        if(die.inputMap_value == InputMapStatus_OPTIONAL): #InputMapStatus.OPTIONAL.value
            currRating += -0.01

        #Flag to checK: There needs to be atleast 1 Must touch die, that is not allready touched. 
        if(die.is_mandatory and die.touchdown == 0):
            new_mandatory_td_Flag = True

    #If value is still False -> no new Element Touchdown will be covered. Return ImpossibleValue
    if new_mandatory_td_Flag == False:
        return IMPOSSIBLE_VALUE_NEGATIVE


    return currRating


"""These Checks kinda expensive with 3 for Loops. Instead we use Flags with single IF statements
 #TODO: Check this beforehand. unnessesscard call
    #If ANY Element of this touchdown has a 0 on InputMap -> NOT ALLOWED
    #if any(die.inputMap_value == InputMapStatus.FORBIDDEN for die in td_Dies): 
    if any(die.inputMap_value == InputMapStatus.FORBIDDEN.value for die in td_Dies): 
        return IMPOSSIBLE_VALUE_NEGATIVE
        #print("Some Inputmap value was 0")

    #If every bin We are about to Touch allready got a touchdown -> No new Bins -> No GAIN
    if all(die.touchdown != 0 for die in td_Dies): 
        return IMPOSSIBLE_VALUE_NEGATIVE
        #print("There are no dies without touchdown allready", ','.join(str(obj.touchdown) for obj in td_Dies))

    #There needs to be atleast 1 Must touch die, that is not allready touched. 
    #if (any(die.inputMap_value == InputMapStatus.MANDATORY and die.touchdown == 0 for die in td_Dies) == False): 
    if (any(die.is_mandatory and die.touchdown == 0 for die in td_Dies) == False): 
        return IMPOSSIBLE_VALUE_NEGATIVE
        #print("No new Die was covered where no Touchdown was before", ','.join(str(obj.inputMap_value) for obj in td_Dies), ','.join(str(obj.touchdown) for obj in td_Dies))

"""