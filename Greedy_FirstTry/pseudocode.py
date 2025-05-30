Pseudocode:
GreedyMain.py


loadData() #get Probecard, InputMap
waferMapObj = WaferMapClass() #contains problem Variables / Maps
solutionMapsObj = SolutionMapsClass() # contains touchdownMap, ratingsMap, leastFlexibleMap...

#MainLoop
while(allBinsCovered == False and maxDepthReached == False):
    x,y = select_next_rouchdown()

    placeTouchdown(x,y)

    update_values_after_touchdown(x,y )
    



def select_next_rouchdown():
    #get List of all Elements of leastFlexibleMap that are Value 1
    leastFlexibleBins = np.argwhere(leastFlexibleMap) 
    if(leastFlexibleBins.size >= 1): 
        return random.selectElement(leastFlexibleBins)
    
    #get List of all Elements that have the highest Rating
    maxRatingBins = np.argwhere(ratingsMap == max(ratingsMap)) 
    return random.selectElement(maxRatingBins)


def update_values_after_touchdown(x,y):
    # Mask is a minkowski Sum of Probecard + Probecard etc. 
    # Contains calculated coordinates, so we can Update around x/y instead of ALL Values
    for x,y in probecard_mask1:
        updateTouchdownRating(x, y)

    for x,y in probecard_mask5:
        updateTouchdownRating(x, y)
        updateLeastFlexbile(x,y)
"""
Example 1: 2x3 Probecard
Cover 1
[[1 1]
 [1 1]
 [1 1]]

Cover5:
 [[1 1 1 1]
 [1 1 1 1]
 [1 0 0 1]
 [1 0 0 1]
 [1 0 0 1]
 [1 1 1 1]
 [1 1 1 1]]

Example 2: Star Probecard
 Cover1 : 
 [0 1 0]
 [1 1 1]
 [0 1 0]]
Cover5:
 [0 0 0 1 0 0 0]
 [0 0 1 1 1 0 0]
 [0 1 1 0 1 1 0]
 [1 1 0 0 0 1 1]
 [0 1 1 0 1 1 0]
 [0 0 1 1 1 0 0]
 [0 0 0 1 0 0 0]]
 """