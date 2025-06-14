# WaferCovering_Heuristics
This is the subfolder *Genetic Algorithm* of the git repository for the article "Heuristic Approaches to the Wafer Covering Problem." This subfolder contains several classes to enhance the genetic algorithm provided by pymoo.

## Dependencies
Besides standard python libraries, the code is based on the ibraries *pymoo* and *multiprocessing*.

## Running the code 
A full experiment for all instances of the problem suite can be started using the *GeneticMain.py*. Results are written to the DATA subfolder. To avoid overwriting olddata, use a new versionID for each run.
A single run can be started with the *GeneticSingleRun.py*. The specific instance can be specified in the file. No output is saved to a file, but more detailed results are given on the command line.