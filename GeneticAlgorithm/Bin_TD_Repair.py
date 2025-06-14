import sys; import os

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '..') )) # path for wafer / probe card libraries and Greedy_Optimized

from Greedy_Optimized.Probecard.getProbecardByName import getProbecardByName
from Greedy_Optimized.GreedyInit import init_greedy_data
from Greedy_Optimized.GreedyLoop import Greedy_Loop
from Greedy_Optimized.Solution.WeightSettingsClass import WeightSettingsClass
from inputMapsLibary import *
from probecardLibary import probecardDict_ForTesting
import Bin_TD_Problem

from pymoo.core.repair import Repair

import numpy as np
from typing import Tuple
import datetime as dt
import math
import random as rd
import multiprocessing as mp
import time
import copy
import cpmpy as cp

# improve a solution by exactly solving the neighborhood of the worst touchdown
## problem: current problem instanc [Bin_TD_Problem object]
## site1Map: binary array of touchdown positions [waferSize x waferSize]
def cspImprovement(problem, site1Map):
    tdc = problem.toTdCounts(site1Map)
    row = copy.deepcopy(site1Map)

    # Calculate individual touchdown penalties and identify worst contributor
    tdPenalties = dict()
    worstIndex, worstPenalty = None, -np.infty
    for j in np.argwhere(row)[:, 0]:
        (touchX, touchY) = problem.validOptions[j]
        thisPenalty = sum( 2**(tdc[touchX+probeX, touchY+probeY]-1) 
                                                    for (probeX, probeY) in problem.probecard 
                                                    if problem.wafer[touchX+probeX, touchY+probeY] == 1 )
        tdPenalties[ (touchX, touchY) ] = thisPenalty
        if thisPenalty > worstPenalty:
            worstIndex = j
            worstPenalty = thisPenalty

    (worstX, worstY) = problem.validOptions[worstIndex]
        
    # remove worst touchdown and close neighbors
    minX, maxX = min(p[0] for p in problem.probecard), max(p[0] for p in problem.probecard)
    minY, maxY = min(p[1] for p in problem.probecard), max(p[1] for p in problem.probecard)
    xLen, yLen = maxX - minX+1, maxY - minY+1

    left, right = worstX - xLen, worstX + xLen
    down, up = worstY - yLen, worstY + yLen

    tdcCopy = np.copy(tdc)
    for j in range(len(problem.validOptions)):
        (touchX, touchY) = problem.validOptions[j]
        if row[j] and left <= touchX and touchX <= right and down <= touchY and touchY <= up:
            row[j] = False
            for (probX, probY) in problem.probecard:
                tdcCopy[touchX + probX, touchY + probY] -= 1

    leftBound, rightBound = max(0, left - (xLen-1)), min(right + (xLen-1), problem.wafer.shape[0])
    downBound, upBound = max(0, down - (yLen-1)), min(up + (yLen-1), problem.wafer.shape[1])

    tdcCopy = tdcCopy[ leftBound:rightBound+1, downBound:upBound+1 ]
    waferCopy = np.copy(problem.wafer)
    waferCopy = waferCopy[ leftBound:rightBound+1, downBound:upBound+1 ]

    # construct CP model and call solver
    dieCount = sum( (waferCopy[i, j] == 1) for (i, j) in np.ndindex(waferCopy.shape))

    probecardPos = cp.IntVar( 0, 1, shape = waferCopy.shape, name = "pPos" )
    touchCount = cp.IntVar( 0, len(problem.probecard), shape = waferCopy.shape, name = "tCount" )

    ### Creating Model
    model = cp.Model()
    xl, xu = 0, waferCopy.shape[0]
    yl, yu = 0, waferCopy.shape[1]
    
    # Condition 1: Only permissible touchdowns - List is 0 for allowed space. 1 for not allowed
    model += [  probecardPos[x, y] == 0
        for (x, y) in np.ndindex(waferCopy.shape)
        if any( x+p[0] > xu - 1 for p in problem.probecard ) or any( x+p[0] < 0 for p in problem.probecard ) or
            any( y+p[1] > yu - 1 for p in problem.probecard ) or any( y+p[1] < 0 for p in problem.probecard ) or 
            any( waferCopy[x+p[0], y+p[1]] == 0 for p in problem.probecard )
            ]

    # Condition 2: for every position, the number of touchdowns has to be calculated 
        # -> Take the sum for every cell of all probecard options that could touch this die
        # additionally, add the previous tdc (since this is a non-initial solution)
    model += [ touchCount[x, y] == sum( probecardPos[(x-p[0]), (y-p[1])] for p in problem.probecard 
                                if x-p[0]>=xl and y-p[1]>=yl and x-p[0]<xu and y-p[1]<yu ) + tdcCopy[x, y]
                            for (x, y) in np.ndindex(waferCopy.shape)
            ]

    # Condition 3: Every must-test die is touched at least once
    model += [ touchCount[x, y] >= 1
                for (x, y) in np.ndindex(waferCopy.shape)
                if(waferCopy[x][y] == 1)
            ]

    objective = cp.IntVar( dieCount, pow(2, 2) * dieCount, name = "pSum")
    model += [ objective >= sum( (touchCount[x, y] == i) * pow(2, i-1)
                for (x, y) in np.ndindex(waferCopy.shape)
                for i in range(1, len(problem.probecard)+1)
                if waferCopy[x, y] == 1 ) ]
    model.minimize(objective)

    solver = cp.solvers.CPM_ortools(model)
    solver.solve(max_time_in_seconds = 10, log_search_progress=False, num_search_workers = 1) # , num_search_workers = parallelWorkers

    model_status = solver.status()
    if model_status.exitstatus.value != 2:
        """print("cpmpy has not found the optimal solution!")
        print(model_status)"""
        return site1Map

    # reinsert solution back into original array
    tdPos = np.argwhere(probecardPos.value())
    tdPos = [ (leftBound + t_x, downBound + t_y) for (t_x, t_y) in tdPos ]
    for (touchX, touchY) in tdPos:
        touchIndex = problem.validOptions.index( (touchX, touchY) )
        row[touchIndex] = True

    return row

# repair solution by passing it to the greedy algorithm
def greedyRepair(problem, x):
    curr_weight = [20, 80, 0]
    weightSettingsObj = WeightSettingsClass(weight_score_gain=curr_weight[0], weight_adjacent_flex_sum=curr_weight[1], weight_forbidden_distance_and_optional_covered_static=curr_weight[2])

    placedTouchdowns = dict()
    tdCounter = 0
    for i in range(len(problem.validOptions)):
        if x[i]:
            placedTouchdowns[tdCounter] = problem.validOptions[i]
    waferObj, solutionObj = init_greedy_data(problem.waferArg, problem.probecardArg, placedTouchdowns, weightSettingsObj)
    resultObj = Greedy_Loop(waferObj, solutionObj, dt.timedelta())

    return [ (site1 in resultObj.td_Location_List) for site1 in problem.validOptions ]

# repair solution by iterating over set and picking random valid touchdown for any untouched die
def fastRepair(problem, x, cspFlag):
    tdCounts = problem.toTdCounts(x)
    allTouchdowns = set( [problem.validOptions[i] for i in range(len(problem.validOptions)) if x[i] ] )

    assert tdCounts.shape == problem.wafer.shape

    # find all required dies that are not touched by the initial solution
    reqUntouched = []
    for (i, j) in np.ndindex(tdCounts.shape):
        if problem.wafer[i, j] == 1 and tdCounts[i, j] == 0:
            reqUntouched.append( (i,j) )

    reqUntouched = set(reqUntouched)

    # repeatedly pick a random untouched required die and choose a non-dominated valid touchdown for it
    while len(reqUntouched) > 0:
        (nextX, nextY) = rd.choice( list(reqUntouched) )
        """tdOptions = [(nextX - probX, nextY - probY) 
                    for (probX, probY) in problem.probecard 
                        if not any(problem.wafer[nextX-probX+pX, nextY-probY+pY] == 0 for (pX, pY) in problem.probecard)
                ]"""
        
        bestTD, bestVal = None, - np.inf
        for (probX, probY) in problem.probecard:
            if not any(problem.wafer[nextX-probX+pX, nextY-probY+pY] == 0 for (pX, pY) in problem.probecard):
                eval = problem.evalTD(tdCounts, nextX-probX, nextY-probY, priori = True)

                if eval > bestVal:
                    bestTD = (nextX-probX, nextY-probY)
                    bestVal = eval

        # randomly pick a non-dominated option
        """(touchX, touchY) = rd.choice(tdOptions)             ###### this choice could be improved ###### """
        (touchX, touchY) = bestTD
        allTouchdowns.add( (touchX, touchY) )
        for (probX, probY) in problem.probecard:
            tdCounts[touchX+probX, touchY+probY] += 1
            if (touchX+probX, touchY+probY) in reqUntouched:
                reqUntouched.remove( (touchX+probX, touchY+probY) )

    # remove redundant touchdowns (i.e. where all touchdown counts are 2 or higher)
    ## check touchdowns in a random order    
    tdEvals = {(touchX, touchY): problem.evalTD(tdCounts, touchX, touchY, priori = False) for (touchX, touchY) in allTouchdowns 
                if all(tdCounts[touchX+probX, touchY+probY] > 1 for (probX, probY) in problem.probecard if problem.wafer[touchX+probX, touchY+probY] == 1) }
    tdList = list(tdEvals.keys())
    tdList = sorted(tdList, key = lambda k: tdEvals[k])
    for (touchX, touchY) in tdList:
        if all(tdCounts[touchX+probX, touchY+probY] > 1 for (probX, probY) in problem.probecard if problem.wafer[touchX+probX, touchY+probY] == 1):
            allTouchdowns.remove( (touchX, touchY) )
            for (probX, probY) in problem.probecard:
                tdCounts[touchX+probX, touchY+probY] -= 1

    # translate remaining touchdowns into a solution
    site1Map = [ (site1 in allTouchdowns) for site1 in problem.validOptions ]

    # if set: solve worst touchdowns with CSP and remove any redundancies afterwards
    if cspFlag:
        site1Map = cspImprovement(problem, site1Map)

        allTouchdowns = [problem.validOptions[i] for i in range(len(problem.validOptions)) if site1Map[i]]
        tdCounts = problem.toTdCounts(site1Map)
        redunEval = {(touchX, touchY): problem.evalTD(tdCounts, touchX, touchY, priori = False) for (touchX, touchY) in allTouchdowns 
                if all(tdCounts[touchX+probX, touchY+probY] > 1 for (probX, probY) in problem.probecard if problem.wafer[touchX+probX, touchY+probY] == 1) }
        tdList = list(redunEval.keys())
        tdList = sorted(tdList, key = lambda k: redunEval[k])
        for (touchX, touchY) in tdList:
            if all(tdCounts[touchX+probX, touchY+probY] > 1 for (probX, probY) in problem.probecard if problem.wafer[touchX+probX, touchY+probY] == 1):
                allTouchdowns.remove( (touchX, touchY) )
                for (probX, probY) in problem.probecard:
                    tdCounts[touchX+probX, touchY+probY] -= 1
                    
        site1Map = [ (site1 in allTouchdowns) for site1 in problem.validOptions ]

    return site1Map

def parallelRepair(problem, X, workerNmbr, cspFlag, **kwargs):
    workerPool = mp.Pool(workerNmbr)
    asyncResults = [ workerPool.apply_async(fastRepair, args=(problem, row, cspFlag)) for row in X ]

    while not(all(r.ready() for r in asyncResults)):
        time.sleep(0.1)

    repairedRows = [res.get() for res in asyncResults]

    return repairedRows

def serialRepair(problem, X, cspFlag, **kwargs):
    repairedRows = [None for _ in X]
    for i in range(X.shape[0]):
        row = X[i]
        
        repairedTouchdowns = fastRepair(problem, row, cspFlag)
        # repairedTouchdowns = greedyRepair(problem, row, cspPeriod)
        repairedRows[i] = repairedTouchdowns

    return repairedRows

class Bin_TD_Repair(Repair):
    def __init__(self, poolNmbr = None, cspImprovement = -1):
        self.workerNmbr = poolNmbr
        self.cspPeriod = cspImprovement 
        self.nextCspImprovement = self.cspPeriod
        super().__init__()

    def _do(self, problem:Bin_TD_Problem, X:np.array, **kwargs):
        # repair every row of x separately by running the greedy loop on it
        assert X.shape[1] == len(problem.validOptions)
        
        if self.workerNmbr is None:
            repairedRows = serialRepair(problem, X, self.nextCspImprovement == 1, **kwargs)
        else:
            repairedRows = parallelRepair(problem, X, self.workerNmbr, self.nextCspImprovement == 1, **kwargs)

        self.nextCspImprovement -= 1
        if self.nextCspImprovement <= 0:
            self.nextCspImprovement = self.cspPeriod

        return np.array(repairedRows)
    

if __name__ == "__main__":
    mp.freeze_support()
    currInputMapFilepath = filepath_51x51_100Percent
    currProbecardSize = "2x3"

    btdProblem = Bin_TD_Problem.Bin_TD_Problem(currInputMapFilepath, currProbecardSize, Bin_TD_Problem.penaltySum )

    x = np.array([[ False for _ in btdProblem.validOptions ] for _ in range(30)])

    leastTouchdowns = math.floor(float(btdProblem.wafer.size) / len(btdProblem.probecard))
    print(f"Ideal least touchdowns: {leastTouchdowns}")

    for i in range(x.shape[0]):
        tdList = np.random.randint(low = 0, high = len(btdProblem.validOptions), size = leastTouchdowns)
        tdList = np.unique(tdList)
        """print("Length TD List:", tdList.shape, leastTouchdowns)"""

        for j in tdList:
            x[i, j] = True

    btdRepair = Bin_TD_Repair(poolNmbr = 6, cspImprovement = 1)
    newX = btdRepair._do(btdProblem, x)
    
    out = dict()
    btdProblem._evaluate(newX, out)
    print(f"Eval: {out['F']}")
    print("avg Eval:", np.mean(out['F']))

    tdNo = [ sum(1 for e in row if e ) for row in newX ]
    print("Number of touchdowns:", tdNo)

    allTdCounts =  [ btdProblem.toTdCounts(row) for row in newX]

    print("All req touched", all( all(tdCount[i,j] > 0 for (i, j) in np.ndindex(tdCount.shape) if btdProblem.wafer[i, j] == 1) for tdCount in allTdCounts ) )
    print("No forbidden touched", all( all(tdCount[i,j] == 0 for (i, j) in np.ndindex(tdCount.shape) if btdProblem.wafer[i, j] == 0) for tdCount in allTdCounts ) )
    
    redundFlag = False
    for k in range(newX.shape[0]):
        row = newX[k]
        tdCount = allTdCounts[k]
        for i in range(row.shape[0]):
            if row[i]:
                (touchX, touchY) = btdProblem.validOptions[i]
                if all(tdCount[touchX+i, touchY+j] > 1 for (i, j) in btdProblem.probecard if btdProblem.wafer[touchX+i, touchY+j] == 1):
                    print("Redundant touchdown found!")
                    redundFlag = True
                    break

    if not redundFlag:
        print("No redundant touchdowns found.")