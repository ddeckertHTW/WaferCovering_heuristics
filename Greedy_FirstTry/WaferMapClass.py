import numpy as np

from Greedy_FirstTry.ProbecardClass import ProbecardClass

class WaferMapClass:
    def __init__(self, inputMap, probecard, prevTdMap = None):
        #Dictionary of my current Wafermap with coordinates as key und Value as 
        #TODO: DICTIONARY IS NOT REALLY USED... DO SOMETHING ELSE!!!
        self.binsDict = {index: DieClass() for index, value in np.ndenumerate(inputMap)} # How to access: self.binsDict[(2,2)]
        self.inputMap = inputMap
        self.probecard: ProbecardClass = probecard

        # Contains only 1 Values in the input Map. Those are the Must Touch Dies
        self.mustTouchMap = np.zeros_like(inputMap)
        self.mustTouchMap[inputMap == 1] = 1 

        #Fill binsDict Values
        self.fillBinsData()
        
        #TouchdownMap from previous TestProject_PT2. Set to an all zero map if no map is given...
        #self.prevTdMap = prevTdMap if prevTdMap is not None else np.zeros_like(inputMap)


    def checkAllBinsCovered(self, currTouchdownMap):
        touchdownsFiltered = currTouchdownMap[self.mustTouchMap == 1]
        return np.all(touchdownsFiltered >= 1)


    #Empty Initializer of the main Dict -> Fill the Data here
    def fillBinsData(self):
        from Greedy_FirstTry.Touchdowns import getAllPossibleTouchdownsMap, getAllPossibleTouchdowns_Strict_NoOptional

        touchdownsPossible = getAllPossibleTouchdownsMap(self.inputMap, self.probecard)
        touchdownsPossible_Strict = getAllPossibleTouchdowns_Strict_NoOptional(self.inputMap, self.probecard)

        #testMap = np.zeros_like(self.inputMap)
        #Fill in all the Values in the loop
        for x, y in np.ndindex(self.inputMap.shape):
            self.binsDict[(x, y)].inputMapValue = self.inputMap[x, y]

            #touchdownPossible Represents if the touchdown in this coordinate AS SITE 1 would be possible. Not if the die can be covered at all
            #touchdownPossible MEANS if the Touchdown as SITE 1 would be ok. Depending on probecard offset. This may lead to non symetric Tables. IS DIFFERENT FROM INPUT MAP
            self.binsDict[(x, y)].touchdownPossible = touchdownsPossible[x, y]
            #Pur is experimental. To Check all Bins for Strict Least Flexible
            self.binsDict[(x, y)].touchdownPossible_Strict = touchdownsPossible_Strict[x, y]



    # Shows how to filter the Dict Values 
    def getAllPossibleTouchdowns(self):
        return {key: value for key, value in self.binsDict.items() if value.touchdownPossible == 1}
         

    def getAllMandatoryTouchdowns(self):
        return {key: value for key, value in self.binsDict.items() if value.inputMapValue == 1}


    def getAllPossibleMandatoryTouchdowns(self):
        return {key: value for key, value in self.binsDict.items() if value.inputMapValue == 1 and value.touchdownPossible == 1}

    def getAllPossibleMandatoryPureTouchdowns(self):
        return {key: value for key, value in self.binsDict.items() if value.inputMapValue == 1 and value.touchdownPossible == 1 and value.touchdownPossible_Strict == 1}


    def is_touchdown_possible_and_mandatory_coords(self, x, y):
        if (x, y) in self.binsDict:
            return (self.binsDict[(x, y)].inputMapValue == 1 and self.binsDict[(x, y)].touchdownPossible == 1)
        else:
            return None

    def is_touchdown_possible_coords(self, x, y):
        if (x, y) in self.binsDict:
            return self.binsDict[(x, y)].touchdownPossible == 1
        else:
            return None

    def is_touchdown_mandatory_coords(self, x, y):
        if (x, y) in self.binsDict:
            return self.binsDict[(x, y)].inputMapValue == 1
        else:
            return None

    def printTouchdownPossible(self):
        printString = ""
        for x in range(self.inputMap.shape[0]):
            for y in range(self.inputMap.shape[1]):
                printString += f"{self.binsDict[(x, y)].touchdownPossible} "

            printString += "\n"

        print(printString)
        

class DieClass:
    def __init__(self):
        self.inputMapValue = None # Original Value in Input Map
        self.touchdownPossible = None # True / False if based on Probecard a Touchdown is even possible within allowed InputMap bounds (1/2)

    def __str__(self):
        return f"inputMap: {self.inputMapValue} | TdPossible: {self.touchdownPossible}"

    def __repr__(self):
        return f"inputMap: {self.inputMapValue} | TdPossible: {self.touchdownPossible}"
