from typing import List

import numpy as np
from GlobalConstants import InputMapStatus_FORBIDDEN, InputMapStatus_OPTIONAL
from Greedy_Optimized.Probecard import ProbecardClass
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass


# We want to reward Touchdowns, that cover optional Dies.  This makes Touchdowns more likely to be placed on the optional Border
# Which means, that the maximum available Room is used and Mandatory Dies in the Middle have more Room to disperse double Touchdowns
# The more Optonal Dies -> The Bigger the Reward

def get_optional_covered_buff_static(td_dies: List[DieClass]):
    #Count the Amount of Optional Dies, this Touchdown would cover
    count = sum(1 for die in td_dies if die.inputMap_value == InputMapStatus_OPTIONAL)
    return count

