import numpy

"""
Class for all the validation methods
"""
class Validate:

    def populations(self, populations:numpy.array) -> None:
         """
         validate populations
         """
         for population in populations:
            self.single_population(population)
    
    
    def single_population(self, population:numpy.array) -> None: 
        """
        validate single population
        """
        prev_population_lenth = 0
        if (prev_population_lenth !=0 and len(population)!=prev_population_lenth) or len(population)==0:
            raise ValueError(f"Invalid number of Population entries!") 
        if len(list(filter(lambda x: x<0, population)))>0:
            raise ValueError("A Population entry cannot be a negative values!") 
        prev_population_lenth = len(population)

    def year(self, year:int, year_range:list) -> None:
        """Public method to validate year """ 
        if year not in range(year_range[0], year_range[1]+1):
            raise ValueError(f"Year should be between {year_range[0]} and {year_range[1]}!")