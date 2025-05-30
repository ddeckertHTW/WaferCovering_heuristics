import numpy as np

class ProbecardMaskClass:
    def __init__(self, maskArray, setList, xOffset, yOffset):
        self.print_array = maskArray #NP Array
        self.mask_array = np.array(setList) #NP Array for getValueByMask and such

        self.set_list = setList  # List of (0,0) (1,1) etc...
        self.x_offset = xOffset  # Offset to (0,0) Coordinates
        self.y_offset = yOffset  # Offset to (0,0) Coordinates

        self.len = len(setList)

        #If still no usage - remove them
        #self.xSize = maskArray.shape[0]
        #self.ySize = maskArray.shape[1]
