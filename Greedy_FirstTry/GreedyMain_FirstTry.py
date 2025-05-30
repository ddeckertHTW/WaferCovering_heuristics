#region All Imports
import copy
import datetime
import numbers
import os
import random
import sys
import numpy as np

# My Classes
#To be able to import inputMaps or probecardLibary I have to this cursed ****
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from Greedy_FirstTry.selectNextTouchdown import select_next_touchdown_coords, select_starting_touchdown_coords
from Greedy_FirstTry.SolutionMapsClass import SolutionMapsClass


from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE

from Greedy_FirstTry.Touchdowns import getOnlyTouchdownByCoord, placeTouchdownOnPos
from Greedy_FirstTry.WaferMapClass import WaferMapClass
from Greedy_FirstTry.ProbecardClass import ProbecardClass, getProbecardByName
from Greedy_FirstTry.HelperFunc.log_Message import logMessage, printTimestampDiff
from Greedy_FirstTry.HelperFunc.pretty_Print_Array import prettyPrintArray, printArray_Color_Domninaz_Adjacent_FlexSum, printArray_Color_Td_Flex_Rating, printArrayParallel_2, printArrayParallel_3, printArrayParallel_3_Color, printSolutionMapObj_timeline
from Greedy_FirstTry.SaveResult import saveResultJson

from inputMapsLibary import *

#endregion All Imports
prevTDMap_15x15 = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])


################# OPTIONS #################
#Options what WaferMap and Probecard gets loaded. -> In the Files inputMapsLibary.py AND probecardLibary.py

script_dir = os.path.dirname(os.path.abspath(__file__))
DataFolderPath = os.path.join(script_dir, '..', 'Data_Greedy')
DataFolderPath = os.path.join(script_dir, '..')

currInputMapFilepath = filepath_15x15_100Percent
#currInputMapFilepath = filepath_151x151

#New USeCases
#currInputMapFilepath = "/15x15_WaferMap/15x15_Diagonal_Error_InputMap.txt"
#currInputMapFilepath = "/15x15_WaferMap/15x15_Mod4_Error_InputMap.txt"

#currProbecardSIze = "4x4" 
currProbecardSIze = "2x3"
currProbecardSIze = "star"
#currProbecardSIze = "2x8"

prevTdMap = prevTDMap_15x15
prevTdMap = None

#random.seed(42)

def printMap_ToUseForPlot(currMap):
    mapCopy = copy.deepcopy(currMap)

    filter = np.isin(mapCopy, [IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE, None])
    mapCopy[filter] = +0

    print(np.array2string(mapCopy, separator=', '))


#Skalaerer Vektor als Bewertung bauen
#-> Gewicht*X Gewicht*Y -> Daraus summe als Bewertung
def solutionRating(currTouchdownMap):
    filtered_values = currTouchdownMap[np.where(currTouchdownMap != 0)]
    unique_values, counts = np.unique(filtered_values, return_counts=True)
    return dict(zip(unique_values, counts))
    #return np.sum(currTouchdownMap)


#Returns True if solvable. Returns False if any bin that is must touch cannot be touched
def isSoluitionPossible(inputMap, leastFlexibleBin):
    #If ANY Bin that must be touched inputMap == 1. Has NO possible Touch Options (leastFlexibleBin Map). 
    if(np.any(leastFlexibleBin[inputMap == 1] == 0)):
        return False
    return True


def mainGreedy_FirstTry(inputMapFilepath, probecardSize, saveResults=False, debugPrint = False, max_depth_count=10000, solution_attempts = 1):
    startTime = datetime.datetime.now()
    logMessage(f"Start GreedyMain: {inputMapFilepath} InputMap - {probecardSize} PC")

    #Load all Input Data. 
    inputMap =  np.loadtxt(inputMapFilepath, dtype=int)  #2D np Array of InputMap
    #inputMap = np.loadtxt(DataFolderPath + "/" +inputMapFilepath, dtype=int)  #2D np Array of InputMap
    probecard = getProbecardByName(probecardSize)

    #Main Object with all WaferMap Info for this Run
    waferMapObj = WaferMapClass(inputMap, probecard, prevTdMap)

    #Main Object with all relevant Maps for solving -> Touchdowns, Rating etc.
    solutionMapsObj_init = SolutionMapsClass(waferMapObj.inputMap, waferMapObj, probecard)


    if(isSoluitionPossible(waferMapObj.inputMap, solutionMapsObj_init.least_flexible) == False):
        print(f"!!NOT SOLVABLE!! InputMap: {inputMapFilepath} - Probecard: {probecardSize}\n")
        return


    if (debugPrint):
       # printArrayParallel_3_Color("inputMap, \t\t\t\t\tFlexibleStrict, \t\t\t\t\tLFlexible SUM. Count: " ,
       #             waferMapObj.inputMap, solutionMapsObj_init.least_flexible_strict, solutionMapsObj_init.least_flexible_strict_sum, waferMapObj.probecard, 0, 0)
        printArrayParallel_3_Color("Touchdowns, \t\t\t\t\tLeastFlexible, \t\t\t\t\tRating Map. Count: ",
                                    solutionMapsObj_init.touchdownMap, solutionMapsObj_init.least_flexible, solutionMapsObj_init.ratings, waferMapObj.probecard, 0, 0)

    #Print Array string to copy into Plot_MapWithValues.py
    #printMap_ToUseForPlot(solutionMapsObj_init.dominate_Map)

    logMessage(f"Start Greedy MainLoop")
    solRatings = []
    bestSolution = None
    #Outer Loop for generating multuple "solved" Solutions and compare the different REsults
    for solution_count in range(solution_attempts):
        #copy the init State of our solutionMap
        solutionMapsObj = copy.deepcopy(solutionMapsObj_init)

        #Inner Loop of solving a single Cover. Per Iteration a Touchdown is placed
        depth_loop_count = 0
        while (waferMapObj.checkAllBinsCovered(solutionMapsObj.touchdownMap) == False):
            depth_loop_count = depth_loop_count + 1
            if (depth_loop_count >= max_depth_count):
                print(f"Max Loop Count ({max_depth_count}) reached. Return Null")
                break

            #Coordinates as a array: newTD_coords = [x,y]
            if(depth_loop_count == 1):
                newTD_coords = select_starting_touchdown_coords(waferMapObj, solutionMapsObj, waferMapObj.probecard)
            else:
                newTD_coords = select_next_touchdown_coords(waferMapObj, solutionMapsObj, waferMapObj.probecard)

            #Creates a "hole" 1 to 3
            """
            if(depth_loop_count == 1): newTD_coords = [4,5]
            if(depth_loop_count == 2): newTD_coords = [7,4]
            if(depth_loop_count == 3): newTD_coords = [8,6]
            """
            #if(depth_loop_count == 4): newTD_coords = [5,6] #Creates the double. Would be best one

            #Do Touchdown at newTD Coords 
            placeTouchdownOnPos(waferMapObj.inputMap, solutionMapsObj.touchdownMap, probecard, newTD_coords[0], newTD_coords[1])

            #After placing a random Touchdown from the best options. Recalculate the Rating of the affected map Area
            solutionMapsObj.update_values_after_touchdown(waferMapObj, newTD_coords[0], newTD_coords[1])
            #solutionMapsObj.update_weighted_descicion_values()

            #printMap_ToUseForPlot(solutionMapsObj.least_flexible_strict_sum)
            #printMap_ToUseForPlot(solutionMapsObj.least_flexible_strict_sum2)
            #printMap_ToUseForPlot(solutionMapsObj.least_flexible_strict_sum3)

            if (debugPrint and solution_attempts == 1):
                #printArray_Color_Domninaz_Adjacent_FlexSum(solutionMapsObj, waferMapObj, probecard, newTD_coords[0], newTD_coords[1])
                printArray_Color_Td_Flex_Rating(solutionMapsObj, waferMapObj, probecard, newTD_coords[0], newTD_coords[1])


                #printArrayParallel_3_Color("least_flexible_strict_sum, least_flexible_strict_sum2, least_flexible_strict_sum3 ", solutionMapsObj.least_flexible_strict_sum, solutionMapsObj.least_flexible_strict_sum2, solutionMapsObj_init.least_flexible_strict_sum3, waferMapObj.probecard, 0, 0)
                #printMap_ToUseForPlot(solutionMapsObj.td_adjacent_flex_sum)
                print("#############################")

                
        #Finished solving a single Cover.
        solutionMapsObj.finalRating = solutionRating(solutionMapsObj.touchdownMap)
        solRatings.append(solutionMapsObj.finalRating)
        if(bestSolution == None or solutionMapsObj.finalRating < bestSolution.finalRating):
            bestSolution = solutionMapsObj


    printTimestampDiff(startTime, f" - Total Time for {solution_attempts} Solutions.")

    if(solution_attempts > 1 and debugPrint):
        printSolutionMapObj_timeline(bestSolution.touchdownLocationsList, solutionMapsObj_init,  waferMapObj)

    if (debugPrint):
        print(f"Solution Ratings / Td Count: {solRatings}")



    # SAVE RESULT TO FILE AS JSON
    if (saveResults):
        totalTime = datetime.datetime.now() - startTime
        saveFilePath = (DataFolderPath + os.path.dirname(inputMapFilepath) + "/" + probecardSize)

        saveResultJson(tdMap=bestSolution.touchdownMap,
                       tdLocations=bestSolution.touchdownLocations,
                       tdLocationsList=bestSolution.touchdownLocationsList,
                       tdCount=np.sum(bestSolution.touchdownMap),
                       rating=str(solutionRating(bestSolution.touchdownMap)),
                       time=totalTime,
                       solution_attempts=solution_attempts,
                       pcSize=probecardSize,
                       inputMapFilepath=inputMapFilepath,
                       saveFilePath=saveFilePath)
        

if __name__ == "__main__":
    #Normal
    mainGreedy_FirstTry(currInputMapFilepath, currProbecardSIze, saveResults=False, debugPrint=True, solution_attempts=1)
    
    #Profiling
    #mainGreedy(currInputMapFilepath, currProbecardSIze, saveResults=False, debugPrint=False, solution_attempts=1)
    
    #Multiple Attempts
    #mainGreedy(currInputMapFilepath, currProbecardSIze, saveResults=False, debugPrint=False, solution_attempts=100)


#TODO: Eine Summierung von mehreren Turchgängen Also z.b. 4 Durchläufe. Wo sich die InputMap nicht ändert und z.b. random erte zu optional werden.!
#TODO: Dominanz hat Bug
# TODO: Rating map wird aktuell zu Impossible Value nach einem TD. Aber DOminanz braucht alle werte egal obs schon ist



######## TODO
#TODO: Init - Vorbereitung in eine Func packen
#DONE: Auto Testing für alle Probecard Größen + WaferMaps kombinationen machen
#       -WaferMap Result
#       -Profiler       
#DONE: AKzeptables Datenformat für Speichern dessen erstellen
#DONE: Akzeptable Ordner Struktur bzw. Datei/Wo/Wie um das zu speichern...
#Done: Globale Variabln wie Probecard und Inputmap anders besser zur verfügung stellen
#TODO: TouchdownClass
#TODO: Bei 2x16 Probecard und 15x15 Wafermap -> Check if possible at all...
#Done: MaxRating und Ratings schauen aktuell noch nicht nach Covering von (1). Werden Touchdowns gesetzt, auch wenn Rating -5 wäre... 
#       Und der einzig fehlende Touchdown halt wegen einem 3x Touchdown Rating von -6 hat...
#TODO: Map entweder nur immer als 2D Array !!!ODER!!! als Dict abspeichern. Nicht beides mischen - used in: WaferMapClass,  getOnlyPossibleTouchdowns
#       Vorteile Dict: easy lookup      Nachteile: Extra rechenzeit + cursed schreibweise
#       Vorteile Array: schnelle Rechenzeit     Nachteile: unübersichtlich/nicht leserlich 
#DONE: Least Flexible Die + 
#TODO: Löcher erschaffen penalizing. -> OPTIMIZE Rating
#TODO: Bessere schreibweise.     for x, y in np.ndindex(probecard.pcArray.shape):
#TODO: RENAME "COVER" TO "MASK"
#TODO: Debug  Probecard: 2x8 für 15x15. Sollte gehen lol

#TODO: REFACTORING
#       In Ordnern Funktionalitäten Bündeln
#       Pro exportierte Funktion eiene Datei machen
#       Naming nach: module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name, query_proper_noun_for_thing, send_acronym_via_https.
#       https://google.github.io/styleguide/pyguide.html#s3.16.3-file-naming

#TODO: Least Flexible mit oder ohne Rand als Filter?

#TODO: Anstatt -99 als NO Value zu nutzen. Ersetzt durch eine einfach #nderbare Globale Variable. Probiere "." oder "-" sowas anstatt...
#   UND Inputmap 0,1,2 VALUES als Variable zum späteren schnellen Ändern einführen...
    #Gibts nen Error wegen Int und string?
    #BOOL IST BEST ->
    #https://miro.medium.com/v2/resize:fit:720/format:webp/1*eGtRdyyxpuh_v-scU6454g.png


#Rating Func Ansätze:
# Least Flexible Die Versionen -> Map erzeugen, die aussagt wie viele Platzierungsmöglichkeit pro Die es gibt 
#   Nur eine möglichkeit für TD die erlaubt ist durch "Not Allowed" Bins in Input Map. Ist immer erzwungen -> hohe priorität
#   Nur eine möglichkeit für TD ohne NEUE doppelte Touchdowns zu erzeigen 
#       -> Alle optionen ohne neue Touchdowns zu bevorzugen, kann zu unvorteilhaften Rissen/offenen Bereichen führen. 
#           Ist mit insgesamt Rating zu kombinieren 
#
#   Rating minus für das Erschaffung von Löchern, wo die Probecard nicht reinpasst, ohne Doppelte Touchdowns zu erzeugen

#https://images.datacamp.com/image/upload/v1676302459/Marketing/Blog/Numpy_Cheat_Sheet.pdf