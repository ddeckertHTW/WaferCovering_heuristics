import numpy as np

# Input: [(0, 1), (1, 1), ...]
# Output: [0, 1] -> A NP Array where the coordinates have the value 1. The Rest 0. Offset is the distance to coord (0,0)
#         [0, 1] 
def convertListToNpArray_WithOffset(coordList):
    min_x = min(coord[0] for coord in coordList)
    max_x = max(coord[0] for coord in coordList)
    min_y = min(coord[1] for coord in coordList)
    max_y = max(coord[1] for coord in coordList)

    # Calculate dimensions of the output array
    rows = max_x - min_x + 1
    cols = max_y - min_y + 1

    # Create a NumPy array of zeros
    output_array = np.zeros((rows, cols), dtype=int)

    # Mark specified coordinates with value 1
    for coord in coordList:
        adjusted_x = coord[0] - min_x
        adjusted_y = coord[1] - min_y
        output_array[adjusted_x, adjusted_y] = 1

    # Offset of where the "original" 0/0 coord is -> -min_x, -min_y
    return output_array, min_x, min_y
