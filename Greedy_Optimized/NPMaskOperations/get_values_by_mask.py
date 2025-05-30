from Greedy_Optimized.Probecard.ProbecardMaskClass import ProbecardMaskClass


def get_values_by_mask(x, y, array, mask: ProbecardMaskClass):
    # Calculate absolute indices by adding the current position (x, y) to the mask
    mask_x = mask.mask_array[:, 0] + x
    mask_y = mask.mask_array[:, 1] + y

    # Ensure indices are within bounds
    valid_indices = (mask_x >= 0) & (mask_x < array.shape[0]) & (mask_y >= 0) & (mask_y < array.shape[1])
    mask_x = mask_x[valid_indices]
    mask_y = mask_y[valid_indices]
    
    # Retrieve values at masked positions
    return array[mask_x, mask_y]