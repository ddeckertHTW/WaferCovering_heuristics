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

class MyOnjectClass:
    def __init__(self):
        self.myMap1 = np.random.rand(150, 150)  # Example large array
        self.myVal = 12


def worker(num, myObj):
    print('Started worker {}'.format(num))

    start_time = time.time()

    time.sleep(5 * random.random())

    elapsed_time = time.time() - start_time
    print(f'finished worker {num} after {elapsed_time:.2f} seconds')

    return myObj.myMap1

def orchestrate_multi_processes_adjustedTemplate(attempt_count, global_timeout_in_seconds, max_simultaneous_processes=multiprocessing.cpu_count()):
    if max_simultaneous_processes == None:
        max_simultaneous_processes = multiprocessing.cpu_count() - 4 #100% CPU kinda not nice -> Max - 2,3,4... To get like 90% CPU Usage
    else:
        max_simultaneous_processes = min(max_simultaneous_processes, multiprocessing.cpu_count())

    myObj = MyOnjectClass()
    
    results = []
    start_time = time.time()
    attempt = 0


    # Using multiprocessing.Pool to manage the worker processes
    with multiprocessing.Pool(processes=max_simultaneous_processes) as pool:
        # Apply async for non-blocking worker execution
        async_results = [pool.apply_async(worker, args=(i+1, myObj)) for i in range(attempt_count)]

        while time.time() - start_time < global_timeout_in_seconds:
            if all(result.ready() for result in async_results):
                break
            time.sleep(0.1)  # Small sleep to avoid busy-waiting

        # If time limit exceeded, terminate the pool
        if time.time() - start_time >= global_timeout_in_seconds:
            print(f"!! TIMED OUT - Killing all processes.")
            pool.terminate()
        else:
            print(f"All tasks completed within time limit.")

        #Shoule be done automatically...
        pool.close()
        pool.join()

        
    # After timeout, fetch  results that completed
    for i in range(attempt_count):
        try:
            # Attempt to get remaining results without a timeout
            result = async_results[i].get(timeout = 0)
            results.append(result)
            #print("Got Result of Element: ", i)
        except multiprocessing.TimeoutError:
            # If there's still a timeout error, skip it
            #print(f"Process {i} still not completed after timeout.")
            continue


    elapsed_time = time.time() - start_time

    if len(results) >= attempt_count:
        print(f"!! SUCCESS - Reached Attempt COUNT {len(results)}. Final Time: {elapsed_time:.4f} seconds. Saving all additional available Results")
    else:
        print(f"!! TIMED OUT - Reached Attempt COUNT {len(results)}. Final Time: {elapsed_time:.4f} seconds. Saving all additional available Results")
    
    
    return results

# Example usage
if __name__ == "__main__":
    startTime = datetime.datetime.now()

    attempt_count = 10
    global_timeout_in_seconds = 10
    curr_max_simultaneous_processes = 5
    
    #results = orchestrate_multi_processes(attempt_count, global_timeout_in_seconds, max_simultaneous_processes=5)
    results = orchestrate_multi_processes_adjustedTemplate(attempt_count, global_timeout_in_seconds, max_simultaneous_processes = curr_max_simultaneous_processes)
    
    print("Results Len: ", results.__len__())
    printTimestampDiff(startTime, f" - Total Time.")