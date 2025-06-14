import sys; import os

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '..') )) # path for wafer / probe card libraries and Greedy_Optimized

from Greedy_Optimized.Probecard.getProbecardByName import getProbecardByName
from Greedy_Optimized.GreedyInit import init_greedy_data
from Greedy_Optimized.GreedyLoop import Greedy_Loop
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass
from inputMapsLibary import *
from probecardLibary import probecardDict_ForTesting

import Bin_TD_Problem
import Bin_TD_Repair

from pymoo.core.sampling import Sampling

import numpy as np
from typing import Tuple
import datetime as dt
import math

class Bin_TD_Sampling(Sampling):
    def __init__(self, samp_prob = 0.05, repairWorkers = 1, competition = 1.0):
        self.sampleProb = samp_prob
        self.repairWorkers = repairWorkers
        self.competitionSize = 1.0
        super().__init__()

    def _do(self, problem, n_samples, **kwargs):
        # produce larger set of candidates and keep best solutions
        val = np.random.random((math.floor(self.competitionSize * n_samples), problem.n_var))
        X = (val < self.sampleProb).astype(bool)

        if self.competitionSize > 1.0:
            repairOp = Bin_TD_Repair.Bin_TD_Repair(self.repairWorkers, cspImprovement=1)
            X = repairOp._do(problem, X)
            xEval = dict()
            problem._evaluate(X, xEval)

            indList = list(range(xEval['F'].shape[0]))
            indList = sorted(indList, key=lambda i: xEval['F'[i][0]])[:n_samples]
            mask = [i in indList for i in range(X.shape[0])]

            X = X[mask]

        return X