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
    testNo = 5  # number of runs for the same problem instance
    parallelThreads = 6 # number of threads the repair operator can use in parallel
    run_time = "00:01:00" # maximum run time for pymoo ( encoded as hh:mm:ss )
    version = "v3_0" # version id added to the file name
    verbosePrintFlag = True # flag indicating whether calculation steps should be detailed on the command line

    # Hyper-Parameter
    cspPeriods = 20
    bitFlipProb = 0.01
    sampleProb = 0.02 

    # for every test instance (type, wafer size, probe card), perform the set number of runs and aggregate results
    for (testName, testsDict) in testModes.items():
        for (waferName, currInputMapFilepath) in testsDict.items():
            for currProbecardSize in probecardDict_ForTesting:
                btdProblem = Bin_TD_Problem(
                        currInputMapFilepath, 
                        currProbecardSize, 
                        objFct=penaltySum )
                
                if btdProblem.solvable: 
                    resultList = [] 

                    for _ in range(testNo):              
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

                        print(testName, waferName, currProbecardSize)
                        print("Function value: %s" % res.F)

                        if verbosePrintFlag:
                            np.set_printoptions(threshold=sys.maxsize)
                            tdCount = btdProblem.toTdCounts(res.X)
                            print(tdCount)

                            print("All req touched", all( tdCount[i,j] > 0 for (i, j) in np.ndindex(tdCount.shape) if btdProblem.wafer[i, j] == 1) )
                            print("No forbidden touched", all( tdCount[i,j] == 0 for (i, j) in np.ndindex(tdCount.shape) if btdProblem.wafer[i, j] == 0) )

                        # document result
                        objHistory = [ gen.result().F[0] for gen in res.history ]
                        print(objHistory)

                        resultList.append( {
                            "objVal": res.F[0],
                            "t": res.exec_time,
                            "gen": len(res.history), 
                            "sol": [ btdProblem.validOptions[j] for j in np.argwhere(res.X)[:, 0] ],
                            "tdc": btdProblem.toTdCounts(res.X),
                            "hist": objHistory
                        } )

                        print("#################################################")

                    # Save file
                    resultDict = {
                        "Best objective value": min([res["objVal"] for res in resultList]),
                        "Median objective value": np.median([res["objVal"] for res in resultList]),
                        "All objective values": [res["objVal"] for res in resultList], 
                        "Calculation times": [res["t"] for res in resultList], 
                        "Generations": [res["gen"] for res in resultList],
                        "Best results": [res["hist"] for res in resultList],
                        "Best solution": min(resultList, key= lambda x: x["objVal"])["sol"],
                        "Best solution touchdown count": min(resultList, key= lambda x: x["objVal"])["tdc"]
                    }

                    saveFilePath = os.path.join(os.path.join(os.path.dirname(__file__),".."),  "DATA", "Data_Genetic", testName, waferName, currProbecardSize+version+".txt").replace("\\", "/")
                    with open(saveFilePath, 'w') as f:
                        resultString = ", \n".join(f"{a}: {b}" for (a, b) in resultDict.items())
                        np. set_printoptions(threshold=sys. maxsize)
                        print(resultString, file=f)

                else:
                    saveFilePath = os.path.join(os.path.join(os.path.dirname(__file__),".."),  "DATA", "Data_Genetic", testName, waferName, currProbecardSize+version+".txt").replace("\\", "/")

                    print(saveFilePath)

                    with open(saveFilePath, 'w') as f:
                        resultString = "Problem is not solvable!"
                        print(resultString, file=f)

                

                
