
#All relevant Maps (rating, leastFlexible) needed to solve the Problem
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE, InputMapStatus_FORBIDDEN, InputMapStatus_MANDATORY


class DieClass:
    #__init__ values that do not have a default value CAN and MUST be calculated at init of SolutionMapClass. 
    # Anything with Sum (least_flexible_strict_sum) must be done in a second loop because all values must be calcualted for ability to get sum
    def __init__(self, x, y, inputMap_value, td_possible_as_site1, least_flexible = 0, least_flexible_strict = 0, 
                 score_gain = IMPOSSIBLE_VALUE_NEGATIVE, 
                 optional_covered_buff_static = IMPOSSIBLE_VALUE_NEGATIVE, forbidden_distance_static = IMPOSSIBLE_VALUE_POSITIVE,
                 touchdown = 0, adjacent_flex_sum = IMPOSSIBLE_VALUE_POSITIVE, dominate = 0, site1_touchdowns = 0):
        self.x = x
        self.y = y

        #From WaferMapObj as backup. Use is_mandatory instead
        self.inputMap_value = inputMap_value

        # IS TOuchdown HERE as Site1 Possible? Not if it can be touched
        self.td_possible_as_site1 = td_possible_as_site1

        self.is_mandatory = inputMap_value == InputMapStatus_MANDATORY #InputMapStatus.MANDATORY.value
        self.is_mandatory_or_optional = inputMap_value != InputMapStatus_FORBIDDEN #InputMapStatus.FORBIDDEN.value

        #TouchdownCount - how often allready touched
        self.touchdown = touchdown

        # The Score how good this touchdown is. In regard of newly covered Bins versus newly created double Touchdowns
        self.score_gain = score_gain #Impossible Value = IMPOSSIBLE_VALUE_NEGATIVE
  
        #How many options exist to cover this bin without creating a double Touchdown. ONLY WRITE VALUE ON MANDATORY BINS
        self.least_flexible = least_flexible

        #How many options exist to cover this bin without creating a double Touchdown AND without covering a optional Bin
        self.least_flexible_strict = least_flexible_strict

        # Static elements get calculated ONCE but not after touchdown as the Value does not change
        # The Count how many Optional Dies are covered by this Touchdown. The bigger the better
        self.optional_covered_buff_static = optional_covered_buff_static #IMPOSSIBLE_VALUE_NEGATIVE

        # The Average Distance of this Touchdown to the nearest Forbidden Die. The Lower (min 0) the better
        self.forbidden_distance_static = forbidden_distance_static #IMPOSSIBLE_VALUE_POSITIVE


        #After a touchdown adjacent Bins should get a "boost" to avoid gaps / Lücken
        self.adjacent_flex_sum = adjacent_flex_sum # IMPOSSIBLE_VALUE_POSITIVE

        #If Bin cannot be covered anymore without creating a double touchdown -> Find best Touchdown to cover it NOW. In hopes to create less double Touchdowns in the Future
        self.dominate = dominate

        #Location of Site 1 Touchdowns
        self.site1_touchdowns = site1_touchdowns

        # We could "pre" calculate the coordinates of the Maks_1 to get values (excecuted often). Instead of calc this at runtime
        #self.mask1_coords = None
        # Get Values by Mask and this approach are almost identical in speed. (At around 100.000 Loops)
        # For LARGER Calls of getValues (2.000.000) the "pre" calculated Coordinates are a lot faster (smaller PC), but at this point 30 sec vs 40 sec - both are too long
        # For larger Probecards - Values by Mask is faster. But for smaller Probecards the preCalc coords is faster. But there the calc time is just moved to the start
        # Would be implementation of getting values: values = [myArray[coord[0]][coord[0]] for coord in testMap[x][y].linkedCoords]

    def __str__(self):
        return f"{self.x} {self.y}"
    