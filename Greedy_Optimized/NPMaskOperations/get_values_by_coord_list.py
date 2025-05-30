import numpy as np


def get_values_by_coord_list(map: np.array, coordList) -> list:
    valueList = []

    for coord in coordList:
        valueList.append(map[coord[0]][coord[1]])

    return valueList