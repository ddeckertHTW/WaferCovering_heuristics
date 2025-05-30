class probecardMask:
    def __init__(self, coverArray, setList, xOffset, yOffset):
        self.coverArray = coverArray
        self.setList = setList
        self.xOffset = xOffset
        self.yOffset = yOffset

        self.xSize = coverArray.shape[0]
        self.ySize = coverArray.shape[1]
