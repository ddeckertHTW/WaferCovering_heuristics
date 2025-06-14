import sys; import os

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '..') )) # path for wafer / probe card libraries and Greedy_Optimized

from Greedy_Optimized.Probecard.getProbecardByName import getProbecardByName
from Greedy_Optimized.GreedyInit import init_greedy_data
from Greedy_Optimized.GreedyLoop import Greedy_Loop
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass
from inputMapsLibary import *
from probecardLibary import probecardDict_ForTesting
import Bin_TD_Problem

from pymoo.core.crossover import Crossover
from pymoo.util.misc import crossover_mask

import numpy as np
from typing import Tuple
import datetime as dt
import math
import random as rd

class Bin_TD_Crossover(Crossover):
    def _do(self, problem, X, **kwargs):
        # construct mask to split X into 4 quadrants and swap quadrants along one diagonal
        _, n_matings, n_var = X.shape
        M = np.full((n_matings, n_var), False)

        # for every row, pick a crossover point on the wafer and split into quadrants
        xLen, yLen = problem.wafer.shape
        for i in range(n_matings):
            xPoint, yPoint = rd.randrange(1, xLen-1), rd.randrange(1, yLen-1)
            for j in range(len(problem.validOptions)):
                xCoor, yCoor = problem.validOptions[j]
                if (xCoor <= xPoint and yCoor <= yPoint) or (xCoor > xPoint and yCoor > yPoint):
                    M[i, j] = True

        # produce crossover
        Xp = crossover_mask(X, M)

        return Xp
        