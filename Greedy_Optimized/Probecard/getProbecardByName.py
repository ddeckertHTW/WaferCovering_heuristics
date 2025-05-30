from Greedy_Optimized.Probecard.ProbecardClass import ProbecardClass
from probecardLibary import probecardDict

# Get Probecard Array shape from probecardLibary and convert it to ProbecardClass
def getProbecardByName(sizeString):
    # The given String e.g. "2x2" must be present in the probecardLibary.py probecardDict
    return ProbecardClass(probecardDict[sizeString])