import numpy as np
from GlobalConstants import IMPOSSIBLE_VALUE_NEGATIVE, IMPOSSIBLE_VALUE_POSITIVE
from Greedy_Optimized.Solution.WaferMapClass import WaferMapClass
from Greedy_Optimized.Solution.DieClass import DieClass
from Greedy_Optimized.Solution.get_forbidden_distance_static import get_forbidden_distance_static
from Greedy_Optimized.Solution.get_optional_covered_buff_static import get_optional_covered_buff_static


#The Object with the "chaning" Evaluation Values. For each Solution all relevant descicion variables are stored here
class SolutionMapClass:
   def __init__(self, waferMapObj: WaferMapClass):
      # This 2D Die Map in shape of Inputmap will be the Main Map with all Data to solve the Problem
      self.dieMap: np.ndarray[DieClass] = np.empty(shape=waferMapObj.inputMap.shape, dtype=DieClass) # Starting Value is NONE

      #TODO:
      #A 2D map of a custom Datatype cannot be searched efficiently. For decisive Values, where we want to find the max/min -> Use seperate Map
      self.ratings_map = np.full(shape=waferMapObj.inputMap.shape, fill_value=IMPOSSIBLE_VALUE_NEGATIVE, dtype=float) # Score, Adjacent, Border etc. combined
      #self.forced_options_map = np.full(shape=waferMapObj.inputMap.shape, fill_value=0, dtype=float) #Least Flexible, Dominate combined
      
      # Both forced Maps. Default 0. When element is found. Value is 2 +-1 depending on the score of the TD. So for Hits: min 1, Max 3
      self.forced_leastFlex_map = np.full(shape=waferMapObj.inputMap.shape, fill_value=0, dtype=float)
      self.forced_dominante_map = np.full(shape=waferMapObj.inputMap.shape, fill_value=0, dtype=float)

      #A Flag, that skips the update for leastFlexible Values. Once all least_flexible have reached 0 -> can NEVER again place a TD without creating double TD
      #self.skip_least_flexible = False

      #Just the List in what Order the Touchdowns were placed. Save only Site1 coords 
      self.td_Location_List = []

      # Set initial Values for dieMap. ALL elements of this NP Array are of Type DieClass
      self.init_dieMap_values(waferMapObj)


   def init_dieMap_values(self, waferMapObj: WaferMapClass):
      #Import HERE, to avoid circular Import
      from Greedy_Optimized.NPMaskOperations.get_values_by_mask import get_values_by_mask
      from Greedy_Optimized.Solution.get_td_score_gain import get_td_score_gain_by_List

      #Create leastFlexible Maps and calc them efficiently for ALL bins in Wafer. Must be filtered to only use Mandatory ones
      least_flexible_map, least_flexible_map_strict = self.create_least_flexible_maps(waferMapObj)

      for x,y in waferMapObj.get_all_Mandatory_Touchdowns():
         #Write lesatFlex VAlues if coord is Mandatory TD
         self.dieMap[x][y] = DieClass(x, y, inputMap_value = waferMapObj.inputMap[x][y], td_possible_as_site1=waferMapObj.possible_touchdowns_map[x][y],
                                       least_flexible = least_flexible_map[x][y], least_flexible_strict = least_flexible_map_strict[x][y])

      #Fill in the rest dieMap, So no element is NONE. 
      for x,y in np.argwhere(self.dieMap == None):
         self.dieMap[x][y] = DieClass(x, y, inputMap_value = waferMapObj.inputMap[x][y], td_possible_as_site1=waferMapObj.possible_touchdowns_map[x][y])

      #Update all Values that are Sum of other Tables (least_flexible_strict_sum)
      for x, y in waferMapObj.get_all_Possible_Touchdowns():
         td_dies = get_values_by_mask(x, y, self.dieMap, waferMapObj.probecard.mask_1)
         self.dieMap[x][y].optional_covered_buff_static = get_optional_covered_buff_static(td_dies)
         self.dieMap[x][y].forbidden_distance_static = get_forbidden_distance_static(td_dies, waferMapObj)
         self.dieMap[x][y].score_gain = get_td_score_gain_by_List(td_dies)
         
      #return #DONE

   # Loop over all Possible Touchdowns and for every TOuchdown add for all sites to the lestFlexMap. 
   # HERE are even non mandatory touches covered... Must be filtered as leastFlex Value can only contain Mandatry Bins
   def create_least_flexible_maps(self, waferMapObj: WaferMapClass):
      from Greedy_Optimized.NPMaskOperations.get_coordinates_by_mask import get_coordinates_by_mask

      least_flexible_map = np.zeros_like(waferMapObj.inputMap, dtype=int)
      least_flexible_map_strict = np.zeros_like(waferMapObj.inputMap, dtype=int)
      
      #Loop over all Possible Touchdowns and if Touchdown is even Possible as Strict -> Add to strict Map aswell
      for x,y in waferMapObj.get_all_Possible_Touchdowns():
         touched_coords = get_coordinates_by_mask(x, y, least_flexible_map, waferMapObj.probecard.mask_1)
         for coords in touched_coords:
            least_flexible_map[coords[0]][coords[1]] += 1

         if(waferMapObj.is_touchdown_possible_by_coords_strict(x,y)):
               for coords in touched_coords:
                  least_flexible_map_strict[coords[0]][coords[1]] += 1

      return least_flexible_map, least_flexible_map_strict

   #Returns True if all Mandatory Touchdowns are covered    #Name alternative: isSolutionFound isSolved isFullyCovered
   def check_if_solved(self):
      for x, y in np.ndindex(self.dieMap.shape):
         if(self.dieMap[x][y].is_mandatory and self.dieMap[x][y].touchdown < 1):
            return False
      return True
   
      """array_1d = self.dieMap.flatten()
      if(any(die.touchdown == 0 and die.is_mandatory for die in array_1d)):
         return False   
      return True
      """

   #Returns True if NOT solvable. Returns False if solvavle
   def isSoluitionImpossible(self):
      array_1d = self.dieMap.flatten()

      #If ANY Die that must be touched inputMap == 1. Has NO possible Touch Options (leastFlexibleBin Map). 
      return any([die.least_flexible == 0 and die.is_mandatory for die in array_1d])
