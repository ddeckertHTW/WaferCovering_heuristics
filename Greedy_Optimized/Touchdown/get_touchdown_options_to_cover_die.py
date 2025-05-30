from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass

#For a Die coordinate. Find all Site1 Positions, that would touch the current Die
def get_touchdown_options_to_cover_die(x, y, waferMapObj: WaferMapClass):
    #Loop over the Probecard Sites and use the Offset of each SIte to go over all Placement Options
    coordList = []

    for pc_coord in waferMapObj.probecard.binDict.values():
        if(waferMapObj.is_touchdown_possible_by_coords(x - pc_coord[0], y - pc_coord[1]) == True): #Should inputmap be 1 or not? Otherwise edge pieces are falsly LeastFlexible 1
            coordList.append((x - pc_coord[0], y - pc_coord[1]))

    return coordList