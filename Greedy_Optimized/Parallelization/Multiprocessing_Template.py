#https://gist.github.com/tappoz/cb88f7a9d9ba27cfee1e2f03537fac16
import random
import time
import multiprocessing

conf = {}
conf['timeout_in_seconds'] = 5
conf['process_upper_bound_in_seconds'] = 6
conf['num_of_simultaneous_processes'] = 20

def timeout_procs(procs):
  '''
  No matter what, ALL the processes are:
  - either joined
  - or terminated and joined
  '''
  timeout_in_seconds = conf['timeout_in_seconds']
  start = time.time()
  while time.time() - start <= timeout_in_seconds:
    if any(p.is_alive() for p in procs):
      time.sleep(.1)  # Just to avoid hogging the CPU
    else:
      # All the processes are done, break now.
      print('yuppie! all the processes finished on time! :)')
      for p in procs:
        p.join() # make sure things are stopped properly
        print('stopping process {}'.format(p.name))
      break
  else:
    # We only enter this if we didn't 'break' above during the while loop!
    print("timed out, killing all processes")
    for p in procs:
      if not p.is_alive():
        print('this process is already finished: {}'.format(p.name))
      else:
        print('this process MUST be killed: {} (timeout of {} seconds has passed)'.format(p.name, timeout_in_seconds))
        p.terminate()
      print(' -> stopping (joining) process {}'.format(p.name))
      p.join()

def worker(num):
  print('started worker {}'.format(num))
  start_time = time.time()
  time.sleep(conf['process_upper_bound_in_seconds']*random.random())
  elapsed_time = time.time() - start_time
  print('finished worker {} after {} seconds'.format(num, elapsed_time))

def start_procs(num_procs):
  procs = []
  for i in range(num_procs):
    proc_idx = i+1 # so e.g. for 10 processes: index is from 1 (included) to 11 (excluded i.e. 10 included)
    p = multiprocessing.Process(target=worker, args=(proc_idx,), name=('process_' + str(proc_idx)))
    procs.append(p)
    p.start()
    print('starting process {}'.format(p.name))
  return procs

def orchestrate_multi_processes_Template():
  print('the current configuration is: {}'.format(conf))
  num_procs = conf['num_of_simultaneous_processes']
  procs = start_procs(num_procs)
  timeout_procs(procs)

if __name__ == "__main__":
  orchestrate_multi_processes_Template()