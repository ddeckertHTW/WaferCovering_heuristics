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



#Adjust Worker to contain the Main Greedy Loop
def worker(num, result_queue, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, init_time_total, debugPrint):
    if(debugPrint): print('started worker {}'.format(num))
    if(multiprocessing_debugPrint): print('started worker {}'.format(num))

    loop_start_time = datetime.datetime.now()

    #THe solutin Objects are linked. To modify it in Greedy_Loop we need a full Copy
    #curr_solutionObj = copy.deepcopy(solutionObj)

    #resultObj = Greedy_Loop(waferMapObj, curr_solutionObj, init_time_total=init_time_total)
    
    #Write ResultClass Object into the Queue for further evaluation
    #result_queue.put(resultObj)

    testArray = np.zeros(shape=(150,150))
    result_queue.put(testArray)


    if(debugPrint): print(f"finished Process worker {num} after {convert_TimestampDiff_to_string(datetime.datetime.now() - loop_start_time)} seconds")
    if(multiprocessing_debugPrint): print(f"finished Process worker {num} after {convert_TimestampDiff_to_string(datetime.datetime.now() - loop_start_time)} seconds")

    # ?? Delete the object and call the garbage collector
    #del curr_solutionObj
    #gc.collect()

    #sys.exit()

#Start Max available Processes at the Start
def start_processes(num_processes, result_queue, waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, init_time_total, debugPrint):
    processes = []

    for i in range(num_processes):
        proc_idx = i + 1
        p = multiprocessing.Process(target=worker, args=(proc_idx, result_queue, waferMapObj, solutionObj, init_time_total, debugPrint), name=('greedy_process_' + str(proc_idx)))
        processes.append(p)
        p.start()
        if (multiprocessing_debugPrint): print('Introduction Loop: - starting process {}'.format(p.name))

    return processes

#Hard set to see launch of Processes
multiprocessing_debugPrint = True

#waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, debugPrint, max_loop_count = 10000, td_scenario_list = None
def multiprocessing_greedy(waferMapObj: WaferMapClass, solutionObj: SolutionMapClass, init_time_total: datetime.timedelta,
                           attempt_count, global_timeout_in_seconds, max_simultaneous_processes=None, debugPrint = False):
    #Process Count cannot be larger than multiprocessing.cpu_count()
    if max_simultaneous_processes == None:
        max_simultaneous_processes = multiprocessing.cpu_count() - 4 #100% CPU kinda not nice -> Max - 2,3,4... To get like 90% CPU Usage
    else:
        max_simultaneous_processes = min(max_simultaneous_processes, multiprocessing.cpu_count())

    #Worked Before:
    #result_queue = multiprocessing.Queue()

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    
    results = []
    best_result = None
    start_time = time.time()

    attempt = 0

    #Init Processes by maxing out max_simultaneous_processes
    remaining_attempts = attempt_count - attempt
    num_processes = min(max_simultaneous_processes, remaining_attempts)
    processes = start_processes(num_processes, result_queue, waferMapObj, solutionObj, init_time_total, debugPrint)

    # When Process finsihes and returns a value -> restart the Process and add return value to results. 
    # When timeout or attempt_count is reached Terminate all processes
    while attempt < attempt_count and time.time() - start_time <= global_timeout_in_seconds:
        for i, p in enumerate(processes):
            #print(i, p)
            if not p.is_alive():
                p.join()  # Ensure the process has stopped properly
                #print('restarting process {}'.format(p.name))

                if not result_queue.empty():
                    results.append(result_queue.get())
                    attempt += 1
                    if (multiprocessing_debugPrint): print(f"Finished Attempt: {attempt}. Fetched Result")

                new_proc = multiprocessing.Process(target=worker, args=(i+1, result_queue, waferMapObj, solutionObj, init_time_total, debugPrint), name=('greedy_process_' + str(i+1)))
                processes[i] = new_proc
                new_proc.start()
        
        # Avoid hogging the CPU
        time.sleep(0.1)  
    else:
        elapsed_time = time.time() - start_time
        alive_processCount = 0
        for p in processes:
            if p.is_alive():
                alive_processCount += 1
                #print('this process MUST be killed: {} (timeout of {} seconds has passed)'.format(p.name, global_timeout_in_seconds))
                p.terminate()
            p.join()    

        if attempt >= attempt_count:
            print(f"!! SUCCESS - Reached Attempt COUNT {attempt}. Final Time: {elapsed_time:.4f} seconds. Saving all additional available Results")
        else:
            print(f"!! TIMED OUT - Reached Attempt COUNT {attempt} killing all {alive_processCount} processes. Final Time: {elapsed_time:.4f} seconds. Saving all additional available Results")

    #After Finishing
    while not result_queue.empty():
        results.append(result_queue.get())
        if(debugPrint):
            print("After Termination. Saving available Result, that was not yet saved")
    
    #Find the BEST result in the results List

    if(debugPrint):
        for result in results:
            print(f"Multiprocessing Results: TD Count: {result.td_Count} | TD Sum: {result.td_sum} | Score: {result.final_Rating}")

    #best_result = find_lowest_unique_value_count(results)
    return find_lowest_unique_value_count(results)

def find_lowest_unique_value_count(rating_dicts):
    if not rating_dicts:
        return None
     
    # Find the lowest unique value across all arrays
    all_unique_values = set()
    for curr_rating in rating_dicts:
        all_unique_values.add(max(curr_rating.final_Rating.keys()))
    lowest_unique_value = min(all_unique_values)

    # Find the array with the lowest count for this lowest unique value
    lowest_count = float('inf')
    lowest_count_array_index = -1
    for i, curr_rating in enumerate(rating_dicts):
        #Skip if max is now the minimum we are searching for 
        if(max(curr_rating.final_Rating.keys()) != lowest_unique_value):
            continue

        count = curr_rating.final_Rating.get(lowest_unique_value, 0)
        if count < lowest_count:
            lowest_count = count
            lowest_count_array_index = i
        #EdgeCase, when two results have the same count -> Compare the td_sum and take the best
        elif count == lowest_count:
            if rating_dicts[lowest_count_array_index].td_sum < rating_dicts[i].td_sum:
                lowest_count = count
                lowest_count_array_index = i


    return rating_dicts[lowest_count_array_index]
    #return lowest_count, lowest_count_array_index

# Example usage
if __name__ == "__main__":
    startTime = datetime.datetime.now()

    attempt_count = 10
    global_timeout_in_seconds = 15
    results = multiprocessing_greedy(attempt_count, global_timeout_in_seconds, max_simultaneous_processes=5)
    #results = orchestrate_multi_processes(attempt_count, global_timeout_in_seconds)
    print("Results:", results, " Len: ", results.__len__())
