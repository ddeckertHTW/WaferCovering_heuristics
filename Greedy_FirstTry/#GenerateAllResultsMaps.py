import datetime
import os
import sys

from HelperFunc.log_Message import printTimestampDiff
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from Greedy_FirstTry.GreedyMain_FirstTry import mainGreedy_FirstTry
from inputMapsLibary import filepath_100Percent_Dict
from probecardLibary import probecardDict_ForTesting

DataFolderPath = os.getcwd() + "/Data_Greedy/"

#Removes all Not "InPUT" Maps from DataFolderPath
def removeOldMapsFromDir(filterFilepath = None):
    for inputMapFilepath in filepath_100Percent_Dict.values():
        directoryPath = DataFolderPath +  os.path.dirname(inputMapFilepath) + "/"
        filesInDir = os.listdir(directoryPath)

        for file in filesInDir: #Dont remove "Input" Files. And if a filter is set-> ONLY remove the files with filter in Name
            if "Input" not in file and (filterFilepath is not None and filterFilepath in file):
                os.remove((directoryPath + file))

# Re-Generates all COmbinations of Probecard x InputMap and saves them in the DataFolderPath
if __name__ == "__main__":
    filterFilepath = None #Only given filter Name IS deleted AND regenerated
    filterFilepath = "101"

    removeOldMapsFromDir(filterFilepath)
    startTime = datetime.datetime.now()

    for inputMapFilepath in filepath_100Percent_Dict.values():
        if(filterFilepath is not None and filterFilepath not in inputMapFilepath):
            continue #skip if name does not Math filter

        for probecard in probecardDict_ForTesting:
            mainGreedy_FirstTry(inputMapFilepath, probecard, saveResults=True, debugPrint=False, solution_attempts=1)

    printTimestampDiff(startTime, " - Total Time FOR ALL MAPS")


