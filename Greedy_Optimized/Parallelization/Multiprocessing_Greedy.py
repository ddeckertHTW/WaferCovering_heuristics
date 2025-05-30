#ADJUSTED the Multiprocessing Template to fit usecase: A Max Attempt Count and timelimit. 
# Whatever is reached first -> Close Processes and return the Results
import copy
import datetime
import gc
import multiprocessing
import time
import random
import os; import sys

import numpy as np

from Greedy_Optimized.HelperFunc.convert_TimestampDiff_to_string import convert_TimestampDiff_to_string
from Greedy_Optimized.Solution.ResultClass import ResultClass
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Greedy_Optimized.GreedyLoop import Greedy_Loop
from Greedy_Optimized.Solution.SolutionMapClass import SolutionMapClass
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

#Hardcoded for Debugging -> set to see launch/finish of Workers
multiprocessing_debugPrint = False


#Adjust Worker to contain the Main Greedy Loop
def worker(num, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, init_time_total):
    if(multiprocessing_debugPrint): print('started worker {}'.format(num))
    start_time = time.time()

    #THe solutin Objects are linked. To modify it in Greedy_Loop we need a full Copy
    curr_solutionObj = copy.deepcopy(solutionObj)

    #MAIN Greedy Logic in here
    resultObj = Greedy_Loop(waferMapObj, curr_solutionObj, init_time_total=init_time_total)

    if(multiprocessing_debugPrint): print(f"finished worker {num} after {(time.time() - start_time):.3f} seconds")

    return resultObj

# Max Processes get limited by given max_simultaneous_processes.
# If attempt_count is given. Makes no sense to start 10 processes for 2 attempts. So max attemptCount
# If None as input is given -> Take 90% of CPU 
def get_max_simultaneous_processes(max_simultaneous_processes, attempt_count = None):
    if max_simultaneous_processes == None:
        #100% CPU not good for the Rest of the System. Aim at 80-90% CPU

        if attempt_count is not None:
            return min(attempt_count, int(multiprocessing.cpu_count() * 0.90))
        return int(multiprocessing.cpu_count() * 0.90)
    else:
        if attempt_count is not None:
            return min(min(attempt_count, max_simultaneous_processes), multiprocessing.cpu_count())
        return min(max_simultaneous_processes, multiprocessing.cpu_count())


#waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, debugPrint, max_loop_count = 10000, td_scenario_list = None
def multiprocessing_greedy(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, init_time_total: datetime.timedelta,
                           attempt_count, global_timeout_in_seconds, max_simultaneous_processes=None, return_ALL_results = False):
    #Process Count cannot be larger than multiprocessing.cpu_count()
    max_simultaneous_processes = get_max_simultaneous_processes(max_simultaneous_processes, attempt_count)
    #print("max_simultaneous_processes: ",max_simultaneous_processes, " timeout: ", global_timeout_in_seconds, " attempt_count:", attempt_count)
    
    results = []
    start_time = time.time()

    # Using multiprocessing.Pool to manage the worker processes
    with multiprocessing.Pool(processes=max_simultaneous_processes) as pool:
        # Apply async for non-blocking worker execution
        async_results = [pool.apply_async(worker, args=(i+1, waferMapObj, solutionObj, init_time_total)) for i in range(attempt_count)]

        while time.time() - start_time < global_timeout_in_seconds:
            if all(result.ready() for result in async_results):
                break
            # Avoid hogging the CPU
            time.sleep(0.1)

        # If time limit exceeded, terminate the pool
        if time.time() - start_time >= global_timeout_in_seconds:
            pool.terminate()

        #Should be done automatically... But wont hurt to do
        pool.close()
        pool.join()

    # After timeout, fetch  results that completed
    for i in range(attempt_count):
        try:
            # Attempt to get remaining results without a timeout
            result = async_results[i].get(timeout = 0)
            results.append(result)
        except multiprocessing.TimeoutError:
            #print(f"Process {i} still not completed after timeout.") #timeout error -> skip it
            continue


    #elapsed_time = time.time() - start_time
    if len(results) >= attempt_count:
        print(f"[SUCCESS] - Reached Attempt COUNT: {len(results)} (of {attempt_count}).") #Total Time: {elapsed_time:.3f} seconds
    else:
        print(f"[TIMED OUT] - Reached Attempt COUNT: {len(results)} (of {attempt_count}).")
    
    #Cleanup the Results, so that no None Values get returned
    if not results or results.__len__() == 0:
        return None, 0
    
    #Discard any sinlge List Element: result can be wrongly saved as None (when reaching Loop Limit or Exception was thrown)
    results = [element for element in results if element is not None]


    #For Statistical Analysis. All Results are relevant
    if return_ALL_results:
        return results, len(results)
    
    #Otherwise return the best Score of all
    return find_lowest_score(results), len(results)

def find_lowest_score(results):
    #Find the lowerst Score in obj.final_score
    return min(results, key=lambda obj: obj.final_score)

    
# Example usage
if __name__ == "__main__":
    startTime = datetime.datetime.now()
    attempt_count = 10
    global_timeout_in_seconds = 15

    results = multiprocessing_greedy(attempt_count, global_timeout_in_seconds, max_simultaneous_processes=5)

    print("Results:", results, " Len: ", results.__len__())



""" OLD METHOD OF ZIELFUNKTION

#Find the BEST result in the results List
#return find_lowest_unique_value_count(results), len(results)

#Find the lowest maximum touchdown Count. Then find the result with the min of this max touchdown count
def find_lowest_unique_value_count(rating_dicts):
    #Check if dict is None
    if not rating_dicts or rating_dicts.__len__() == 0:
        return None

    #Discard any result that is wrongly saved as None (when reaching Loop Limit or Exception was thrown)
    rating_dicts = [element for element in rating_dicts if element is not None]

    # Find the lowest unique value across all arrays
    all_unique_values = set()
    for curr_rating in rating_dicts:
        all_unique_values.add(max(curr_rating.Rating_Mandatory.keys()))
    lowest_unique_value = min(all_unique_values)

    # Find the array with the lowest count for this lowest unique value
    lowest_count = float('inf')
    lowest_count_array_index = -1
    for i, curr_rating in enumerate(rating_dicts):
        #Skip if max is now the minimum we are searching for 
        if(max(curr_rating.Rating_Mandatory.keys()) != lowest_unique_value):
            continue

        count = curr_rating.Rating_Mandatory.get(lowest_unique_value, 0)
        if count < lowest_count:
            lowest_count = count
            lowest_count_array_index = i
        #EdgeCase, when two results have the same count -> Compare the td_sum_Mandatory and take the best
        elif count == lowest_count:
            if rating_dicts[lowest_count_array_index].td_sum_Mandatory < rating_dicts[i].td_sum_Mandatory:
                lowest_count = count
                lowest_count_array_index = i


    return rating_dicts[lowest_count_array_index]
    #return lowest_count, lowest_count_array_index


"""