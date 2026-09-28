import numpy


class Validate:
    """
    Class for all the validation methods
    """

    def populations(self, populations:list[numpy.ndarray]) -> None:
        """
        validate several populations: each one on its own, and all the same length
        """
        for population in populations:
            self.single_population(population)
        if len({len(population) for population in populations}) > 1:
            raise ValueError("All Populations must have the same number of entries!")
    
    
    def single_population(self, population:numpy.ndarray) -> None: 
        """
        validate single population
        """
        if len(population) == 0:
            raise ValueError("Invalid number of Population entries!") 
        if len(list(filter(lambda x: x<0, population)))>0:
            raise ValueError("A Population entry cannot be a negative values!") 

    def years_match_population(self, years:numpy.ndarray, population:numpy.ndarray) -> None:
        """
        validate that there is exactly one year for each population entry
        """
        if len(years) != len(population):
            raise ValueError(f"Years and Population must be the same length, got {len(years)} years and {len(population)} entries!")

    def year(self, year:int, year_range:list) -> None:
        """Public method to validate year """ 
        if year not in range(year_range[0], year_range[1]+1):
            raise ValueError(f"Year should be between {year_range[0]} and {year_range[1]}!")