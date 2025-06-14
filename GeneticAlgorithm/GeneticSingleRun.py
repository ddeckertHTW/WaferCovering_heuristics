import sys; import os

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '..') )) # path for wafer / probe card libraries and Greedy_Optimized

from Greedy_Optimized.Probecard.getProbecardByName import getProbecardByName
from Greedy_Optimized.GreedyInit import init_greedy_data
from Greedy_Optimized.GreedyLoop import Greedy_Loop
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass
from inputMapsLibary import *
from probecardLibary import probecardDict_ForTesting

from Bin_TD_Problem import Bin_TD_Problem, penaltySum
from Bin_TD_Sampling import Bin_TD_Sampling
from Bin_TD_Repair import Bin_TD_Repair
from Bin_TD_Crossover import Bin_TD_Crossover
from Bin_TD_Termination import Bin_TD_Termination

from pymoo.core.crossover import Crossover
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.termination.default import DefaultSingleObjectiveTermination

import numpy as np
from typing import Tuple
import datetime as dt
import math
from matplotlib import pyplot as plt
import multiprocessing as mp
import json

if __name__ == '__main__': 
    mp.freeze_support()
    testModes = {"Complete": filepath_100Percent_Dict, "TestStructures": filepath_Mod4_Error_Dict, "Contamination": filepath_Diagonal_Error_Dict}
    
    # User-defined variables
    parallelThreads = 6 # number of threads the repair operator can use in parallel
    run_time = "00:01:00" # maximum run time for pymoo ( encoded as hh:mm:ss )
    verbosePrintFlag = True # flag indicating whether calculation steps should be detailed on the command line
    convergenceGraphFlag = True # flag indicating whether a convergence graph should be shown at the end of the calculation

    # Hyper-Parameter
    cspPeriods = 20
    bitFlipProb = 0.01
    sampleProb = 0.02 

    # define problem instance
    testName = "Complete"
    waferName =  "51x51"
    currProbecardSize = "2x3"

    # algorithm setup
    testsDict = testModes[testName]
    currInputMapFilepath = testsDict[waferName]
    
    btdProblem = Bin_TD_Problem(
            currInputMapFilepath, 
            currProbecardSize, 
            objFct=penaltySum )
    
    if btdProblem.solvable:             
        algorithm = GA(
            pop_size=100,
            sampling=Bin_TD_Sampling( sampleProb, repairWorkers = parallelThreads, competition = 1.0 ), 
            crossover=TwoPointCrossover(),
            mutation=BitflipMutation( prob_var = bitFlipProb ),
            repair = Bin_TD_Repair(poolNmbr = parallelThreads, cspImprovement = cspPeriods),
            eliminate_duplicates=True,
            save_history = True
        )

        btdProblem.set_algorithm(algorithm)

        termination = Bin_TD_Termination(max_time = run_time, period = 30)

        res = minimize(
            btdProblem,
            algorithm,
            termination, 
            verbose=verbosePrintFlag,
            save_history=True
        )

        # document result
        print("Problem instance:", testName, waferName, currProbecardSize)
        print("Best objective value:", res.F[0])
        print("Calculation time:", res.exec_time)
        print("Generations:", len(res.history))

        if verbosePrintFlag:
            np.set_printoptions(threshold=sys.maxsize)
            tdCount = btdProblem.toTdCounts(res.X)
            print("Touchdown count map:", tdCount)

            print("All req touched", all( tdCount[i,j] > 0 for (i, j) in np.ndindex(tdCount.shape) if btdProblem.wafer[i, j] == 1) )
            print("No forbidden touched", all( tdCount[i,j] == 0 for (i, j) in np.ndindex(tdCount.shape) if btdProblem.wafer[i, j] == 0) )

        
        # trace convergence
        if convergenceGraphFlag:
            n_evals = np.array([e.evaluator.n_eval for e in res.history])
            opt = np.array([e.opt[0].F for e in res.history])

            plt.title("Convergence")
            plt.plot(n_evals, opt, "--")
            plt.yscale("log")
            plt.show()
                

                
