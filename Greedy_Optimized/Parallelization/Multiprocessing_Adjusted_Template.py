#ADJUSTED the Multiprocessing Template to fit usecase: A Max Attempt Count and timelimit. 
# Whatever is reached first -> Close Processes and return the Results
import datetime
import multiprocessing
import time
import random
import os; import sys

import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HelperFunc.printTimestampDiff import printTimestampDiff


def worker(num, result_queue):
    #print('\t W - started worker {}'.format(num))

    #create a local Copy of the solution and calculate from here
    #curr_solutionObj = copy.deepcopy(solutionObj)

    start_time = time.time()
    #time.sleep(5 * random.random()) #Acceptable good Time
    time.sleep(5 * random.random())
    
    #time.sleep(1) # Try this to see the Processes Order
    elapsed_time = time.time() - start_time
    print('finished worker {} after {} seconds'.format(num, elapsed_time))

    testArray = np.zeros(shape=(150,150))

    result_queue.put(testArray)
    #result_queue.put(random.randint(0, 100))


#Start Max available Processes at the Start
def start_processes(num_processes, result_queue):
    processes = []

    for i in range(num_processes):
        proc_idx = i + 1
        p = multiprocessing.Process(target=worker, args=(proc_idx, result_queue), name=('greedy_process_' + str(proc_idx)))
        processes.append(p)
        p.start()
        print('Starting Loop - starting process {}'.format(p.name))

    return processes


def orchestrate_multi_processes_adjustedTemplate(attempt_count, global_timeout_in_seconds, max_simultaneous_processes=multiprocessing.cpu_count()):
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    #result_queue = multiprocessing.Queue()
    results = []
    start_time = time.time()

    attempt = 0

    #Init Processes by maxing out max_simultaneous_processes
    remaining_attempts = attempt_count - attempt
    num_processes = min(max_simultaneous_processes, remaining_attempts)
    processes = start_processes(num_processes, result_queue)

    # When Process finsihes and returns a value -> restart the Process and add return value to results. 
    # When timeout or attempt_count is reached Terminate all processes
    while attempt < attempt_count and time.time() - start_time <= global_timeout_in_seconds:
        for i, p in enumerate(processes):
            if not p.is_alive():
                print('restarting process {}'.format(p.name))
                p.join()  # Ensure the process has stopped properly

                if not result_queue.empty():
                    results.append(result_queue.get())
                    attempt += 1
                    #print("Added Element to results")

                new_proc = multiprocessing.Process(target=worker, args=(i+1, result_queue), name=('greedy_process_' + str(i+1)))
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
    if not result_queue.empty():
        print("After Termination. Saving available Result, that was not yet saved")

    while not result_queue.empty():
        results.append(result_queue.get())
    
    return results

# Example usage
if __name__ == "__main__":
    startTime = datetime.datetime.now()

    attempt_count = 50
    global_timeout_in_seconds = 15
    #results = orchestrate_multi_processes(attempt_count, global_timeout_in_seconds, max_simultaneous_processes=5)
    results = orchestrate_multi_processes_adjustedTemplate(attempt_count, global_timeout_in_seconds)
    print("Results:", results, " Len: ", results.__len__())
    #for result in results:
    #    print(result)

    printTimestampDiff(startTime, f" - Total Time.")