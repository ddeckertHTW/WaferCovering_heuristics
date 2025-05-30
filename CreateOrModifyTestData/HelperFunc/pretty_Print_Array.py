import numpy as np

def prettyPrintArray(matrixToPrint,localString = ""):
    print(localString,"\n",np.array2string(matrixToPrint, suppress_small=True, formatter={'float': '{:0.4f}'.format})[1:-1])