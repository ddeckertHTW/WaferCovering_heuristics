#Use as Object to save the current Weight Settings
class WeightSettingsClass:
    def __init__(self, weight_score_gain, weight_adjacent_flex_sum, weight_forbidden_distance_and_optional_covered_static):
        #Important
        self.weight_score_gain = weight_score_gain / 100
        self.weight_adjacent_flex_sum = weight_adjacent_flex_sum / 100
        
        #Later
        self.weight_forbidden_distance_and_optional_covered_static = weight_forbidden_distance_and_optional_covered_static / 100
        #self.weight_optional_covered_buff_static = weight_optional_covered_buff_static / 100
        #self.weight_forbidden_distance_static = weight_forbidden_distance_static / 100

    #Overwrite Print Function
    def __str__(self):
        return f"({self.weight_score_gain}, {self.weight_adjacent_flex_sum}, {self.weight_forbidden_distance_and_optional_covered_static} | score={self.weight_score_gain}, adjacent={self.weight_adjacent_flex_sum}, weight_distance_and_optional={self.weight_forbidden_distance_and_optional_covered_static}"