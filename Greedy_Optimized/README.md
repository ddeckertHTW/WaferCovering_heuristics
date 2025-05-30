# WaferCovering_Heuristics
This is the subfolder *Greedy_Optimized* of the git repository for the article "Heuristic Approaches to the Wafer Covering Problem." This subfolder contains several classes to implement the greedy algorithm.

## Dependencies
Besides standard python libraries, the code is based on the ibrary *multiprocessing*.

## Running the code 
A single greedy run can be started with the *GreedyMain.py*. The specific instance can be specified in the file. The results are written to the comand line. If the versionID is higher than the currently-saved version, results are saved to a file in DATA, overwriting the old results. If not, results are not saved to a file.
To start a full experiment, use the *generate_solutions_Multiprocessing.py* in the subfolder *Generate_Data*. If the versionID is higher than the currently-saved version, results are saved to a file in DATA, overwriting the old results. If not, results are not saved to a file.