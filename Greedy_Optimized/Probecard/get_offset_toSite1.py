#Return absolute (x,y) Coord OFfset to the Site1 where we place the Touchdowns
def get_offset_toSite1(binDict, x, y):
    site_1_coords = binDict.get(min(binDict.keys()))
    return (site_1_coords[0] - x, site_1_coords[1] - y)