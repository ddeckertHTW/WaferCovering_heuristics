from Greedy_Optimized.Probecard.ProbecardMaskClass import ProbecardMaskClass
from Greedy_Optimized.Probecard.createMasks import create_probecard_mask_1, create_probecard_mask_2, create_probecard_mask_3, create_probecard_mask_4, create_probecard_mask_5, create_probecard_mask_6, create_probecard_mask_adjacent

# since the wafer is encoded in array notation, it is represented in y-x notation
# probecard has to be flipped to match
def swapXY(probecard):
    return [ (y, x, name) for (x, y, name) in probecard]

class ProbecardClass:
    def __init__(self, probecard):
        probecard = swapXY(probecard)
        #Sanity Check for Probecard Format.
        check_probecard_format(probecard)
        # Site 1 should be at coords 0/0 to make things easy. 
        probecard = adjust_probecard_corrds(probecard)

        #Create dictionary with SiteID as Key. Example: (1,5,2) -> (x:1, y:5, siteId: 2)
        self.binDict = {point[2]: (point[0], point[1]) for point in probecard} # Use by SiteID: for key in probecard.binDict.keys()
        self.sitesCount = len(probecard)
        
        #For decision variables. When doing Sum(touchdown_dies). The Max of leastFlex and score is self.sitesCount. So the sum is self.sitesCount * self.sitesCount
        self.maxSitesSum = self.sitesCount * self.sitesCount

        # Create Masks using Minkowski Sum to mimic affected Touchdown Areas and other Filter Masks for later calculations
        # Pc | Just the Mask of the Probecard itself
        self.mask_1: ProbecardMaskClass = create_probecard_mask_1(self.binDict.values())
        #print("Mask1 Array: \n", self.mask_1.print_array)

        #TODO: MASK2 kann bei LeastFlex oder insgesamt Berechnungen von SUmmern besser eingesetzt werden als aktuell 5x mask1 
        # Pc around a single Die
        self.mask_2: ProbecardMaskClass = create_probecard_mask_2(self.binDict.values())
        #print("Mask2 Array: \n", self.mask_2.print_array)

        # Pc + Pc | Pc around a Probecard
        self.mask_3: ProbecardMaskClass = create_probecard_mask_3(self.binDict.values())
        #print("Mask3 Array: \n", self.mask_3.print_array)

        # Pc + Pc + Pc | The Mask for all elements that are needed for all relevant Informations after a Touchdown
        #SHOULD NOT BE USED??!! FOR WHAT???
        self.mask_4: ProbecardMaskClass = create_probecard_mask_4(self.binDict.values(), self.mask_3.set_list)
        #print("Mask5 Array: ", self.mask_4.print_array)

        # Pc + Pc - Pc | The Mask for all OUTER Elements of Mask3 (substracted by inner Mask0)
        self.mask_5: ProbecardMaskClass = create_probecard_mask_5(self.binDict.values(), self.mask_3.set_list)
        #print("Mask5 Array: \n", self.mask_5.print_array)

        # Pc + Pc + PC - (Pc + PC) | The Mask for all OUTER Elements of Mask4 using Mask3
        self.mask_6: ProbecardMaskClass = create_probecard_mask_6(self.mask_3.set_list, self.mask_4.set_list)
        #print("Mask6 Array: \n", self.mask_6.print_array)

        # Adjacent coordinates to a touchdown | The Mask for the Site1 Coordinates to find adjacent coords
        self.mask_adjacent: ProbecardMaskClass = create_probecard_mask_adjacent(list(self.binDict.values()), self.mask_1, self.mask_4.set_list)
        #print("mask_adjacent Array: \n", self.mask_adjacent.print_array)

"""
Mask1 Array:	Mask2 Array:	Mask3 Array:		Mask4 Array:  				Mask5 Array:		Mask6 Array: 				mask_adjacent Array: 
 [[0 1 0]		[[0 0 1 0 0]    [[0 0 0 1 0 0 0]   [[0 0 0 0 0 1 0 0 0 0 0]		[[0 0 0 1 0 0 0]   [[0 0 0 0 0 1 0 0 0 0 0]	   [[0 0 0 1 0 0 0]
 [1 1 1]		 [0 1 1 1 0]	 [0 0 1 1 1 0 0]	[0 0 0 0 1 1 1 0 0 0 0]		 [0 0 1 1 1 0 0]	[0 0 0 0 1 1 1 0 0 0 0]		[0 0 1 0 1 0 0]	
 [0 1 0]]		 [1 1 1 1 1]	 [0 1 1 1 1 1 0]	[0 0 0 1 1 1 1 1 0 0 0]		 [0 1 1 0 1 1 0]	[0 0 0 1 1 0 1 1 0 0 0] 	[0 1 0 0 0 1 0]
				 [0 1 1 1 0]	 [1 1 1 1 1 1 1]	[0 0 1 1 1 1 1 1 1 0 0]		 [1 1 0 0 0 1 1]	[0 0 1 1 0 0 0 1 1 0 0]		[1 0 0 0 0 0 1]
				 [0 0 1 0 0]]	 [0 1 1 1 1 1 0]	[0 1 1 1 1 1 1 1 1 1 0]		 [0 1 1 0 1 1 0]	[0 1 1 0 0 0 0 0 1 1 0]		[0 1 0 0 0 1 0]
								 [0 0 1 1 1 0 0]	[1 1 1 1 1 1 1 1 1 1 1]		 [0 0 1 1 1 0 0]	[1 1 0 0 0 0 0 0 0 1 1]		[0 0 1 0 1 0 0]
								 [0 0 0 1 0 0 0]]	[0 1 1 1 1 1 1 1 1 1 0]		 [0 0 0 1 0 0 0]]	[0 1 1 0 0 0 0 0 1 1 0]		[0 0 0 1 0 0 0]]
													[0 0 1 1 1 1 1 1 1 0 0]							[0 0 1 1 0 0 0 1 1 0 0]
													[0 0 0 1 1 1 1 1 0 0 0]							[0 0 0 1 1 0 1 1 0 0 0]
													[0 0 0 0 1 1 1 0 0 0 0]							[0 0 0 0 1 1 1 0 0 0 0]
													[0 0 0 0 0 1 0 0 0 0 0]]						[0 0 0 0 0 1 0 0 0 0 0]]
"""


""" Should not bee needed when using binDict.
        #Calculate helping Variables of x/y Values
        x_values = [point[0] for point in probecard]
        y_values = [point[1] for point in probecard]
    
        x_size = max(x_values) - min(x_values)
        y_size = max(y_values) - min(y_values)

        # With Range we want to include the bounary to be able to do range(0,x_range). We have to add 1. 
        x_range = self.x_size + 1 
        y_range = self.y_size + 1
"""
            
############ Small LOCAL Helper Funcs
def check_probecard_format(pc):
    if all(len(item) == 3 for item in pc):
        return True
    elif all(len(item) == 2 for item in pc):
        raise NotImplementedError("Fix current Probecard and Add SiteIds")
    else:
        raise IndexError("Probecard does not have expected 3-dimensional tuples (SiteIds). Example: (1,5,2) -> (x:1, y:5, siteId: 2)")

# Site 1 should be at coords 0/0 to make things easy. Find SiteID 1 and take that as offset for the whole probecard Array
def adjust_probecard_corrds(pc):
    globalOffset = next(elem for elem in pc if elem[2] == 1)
    return [(elem[0] - globalOffset[0], elem[1] - globalOffset[1], elem[2]) for elem in pc]
