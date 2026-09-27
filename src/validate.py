import numpy

"""
Class for all the validation methods
"""
class Validate:

    """ constructor to define some instance vars """
    def __init__(self):
        self._prev_population_lenth = 0

    """ validate populations"""
    def populations(self, populations:numpy.array):
         for population in populations:
            if (self._prev_population_lenth !=0 and len(population)!=self._prev_population_lenth) or len(population)==0:
                raise ValueError(f"Invalid number Population entries!") 
            if len(list(filter(lambda x: x<0, population)))>0:
                raise ValueError("Population cannot have negative values!") 
            self._prev_population_lenth = len(population)
    
    """Public method to validate year """ 
    def year(self, year:int, year_range:list):
        if year not in range(year_range[0], year_range[1]+1):
            raise ValueError(f"Year should be between {year_range[0]} and {year_range[1]}!")