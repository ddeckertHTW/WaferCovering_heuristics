import sys; import os

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '..') )) # path for wafer / probe card libraries and Greedy_Optimized

from Greedy_Optimized.Probecard.getProbecardByName import getProbecardByName
from inputMapsLibary import *
from probecardLibary import probecardDict_ForTesting

from pymoo.core.problem import Problem

import numpy as np
from typing import Tuple

def penaltySum(tdc):
    return sum(2**(v-1) for v in tdc.flatten() if v > 0)


class Bin_TD_Problem(Problem):
    def __init__(self, wafer, probecard, objFct, **kwargs):
        #Load wafer
        self.wafer = np.loadtxt(wafer, dtype=int)  #2D np Array of InputMap
        self.waferArg = wafer

        self.reqDies = [(y, x) for y in range(self.wafer.shape[0]) for x in range(self.wafer.shape[1]) if self.wafer[y, x] == 1]

        #Load Probecard
        self.probecard = getProbecardByName(probecard).mask_1.set_list
        self.probecardArg = probecard

        # save objective function
        self.objFct = objFct

        # find number of valid touchdowns
        self.validOptions = [ (x, y) 
                                for x in range(self.wafer.shape[0])
                                for y in range(self.wafer.shape[1])
                                        if all(self.wafer[x+p[0], y+p[1]] != 0 for p in self.probecard) ]
        
        # Set algorithm to None
        self.algorithm = None

        # check solvability
        self.solvable = True
        for (reqX, reqY) in self.reqDies:
            if not any(any( (reqX, reqY) == (touchX + p_x, touchY + p_y) for (p_x, p_y) in self.probecard ) for (touchX, touchY) in self.validOptions ):
                self.solvable = False
                break

        # use super constructor
        super().__init__(n_var = len(self.validOptions), n_obj = 1,  n_ieq_constr=0, vtype=bool, **kwargs)

    def countUntouchReq(self, x):
        tdCount = self.toTdCounts(x)
        return sum(1 for (i, j) in np.ndindex(tdCount.shape) if self.wafer[i, j] == 1 and tdCount[i, j] == 0)
    
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def toTdMap(self, x):
        touchdownMap = np.zeros_like(self.wafer)

        # calculate touchdown count on all required dies
        for i in range(len(self.validOptions)):
            if x[i]:
                opt_x, opt_y = self.validOptions[i]
                touchdownMap[opt_x, opt_y] = 1

        return touchdownMap
    
    def toTdCounts(self, x, onlyRequired = False):
        touchdownCount = np.zeros_like(self.wafer)

        for i in range(len(self.validOptions)):
            if x[i]:
                opt_x, opt_y = self.validOptions[i]
                for (p_x, p_y) in self.probecard:
                        if (not onlyRequired) or self.wafer[opt_x + p_x, opt_y + p_y] == 1:
                            touchdownCount[opt_x + p_x, opt_y + p_y] += 1

        return touchdownCount

    def evalTD(self, tdCount, x, y, priori = False, **kwargs):
        # check if evaluation is a-priori (i.e. touchdown has not been made) or a-posteriori
        ## for a-priori, touching a required die is needed if it is not otherwise touched
        if priori:
            reqNeeded = 0
        else:
            reqNeeded = 1

        # check all touched dies: if required and redundant -> penalty | if required and needed -> reward
        eval = 0
        for (probX, probY) in self.probecard:
            if self.wafer[x+probX, y+probY] == 1 and tdCount[x+probX, y+probY] > reqNeeded:
                eval -= 2**tdCount[x+probX, y+probY]
            if self.wafer[x+probX, y+probY] == 1 and tdCount[x+probX, y+probY] <= reqNeeded:
                eval += 5

        return eval
        

    def _evaluate(self, X, out, *args, **kwargs):
        evaluations = []
        constraints = []

        # calculate touchdown count on all required dies
        for row in X:
            touchdownCount = self.toTdCounts(row, onlyRequired = True)

            """# calculate constraint violations (i.e. required dies that were not touched)
            untouchedReq = sum(1 for (i, j) in np.ndindex(touchdownCount.shape) if self.wafer[i, j] == 1 and touchdownCount[i, j] == 0)
            constraints.append(untouchedReq)"""

            # apply objective function
            evaluations.append(self.objFct(touchdownCount))

        out["F"] = np.array(evaluations)
        """out["G"] = np.array(constraints)"""


if __name__ == "__main__":
    currInputMapFilepath = filepath_15x15_100Percent
    currProbecardSize = "2x3"

    btdProblem = Bin_TD_Problem(currInputMapFilepath, currProbecardSize, penaltySum )

    print(btdProblem.wafer)
    print(btdProblem.probecard)

    print(len(btdProblem.validOptions))
    print(btdProblem.validOptions)

    x = np.array([[ False for _ in btdProblem.validOptions ]])
    x[0, 4] = True
    x[0, 1] = True

    out = dict()
    btdProblem._evaluate(x, out)
    print(out)
