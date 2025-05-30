import os

IMPOSSIBLE_VALUE_POSITIVE = 999999
IMPOSSIBLE_VALUE_NEGATIVE = -999999

InputMapStatus_FORBIDDEN = 0
InputMapStatus_MANDATORY = 1
InputMapStatus_OPTIONAL = 2

#New Way
BASE_DATA_FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DATA").replace("\\", "/")
BASE_GREEDY_FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DATA", "Data_Greedy").replace("\\", "/")


#Zielfunktion Parameter
PENALTY_SCORE = 2