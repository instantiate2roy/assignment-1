import math


class ClassroomPlanner:
    """
    Estimate primary-school classrooms from population figures.
    """

    def __init__(self, school_age_share:float = 0.18, class_size:int = 53, population_unit:int = 1):
        """
        Args:
            school_age_share: Share of the population of primary-school age (0.18 = 18%).
            class_size: Pupils one classroom holds.
            population_unit: Multiplier to get headcount, e.g. 1000 if the data is in thousands.
        """
        if not 0 < school_age_share <= 1:
            raise ValueError("School-age share must be between 0 and 1!")
        if class_size <= 0:
            raise ValueError("Class size must be greater than 0!")
        self.__school_age_share = school_age_share
        self.__class_size = class_size
        self.__population_unit = population_unit

    def pupils(self, population:float) -> float:
        """
        Number of primary-school-age children in a population
        """
        return population * self.__population_unit * self.__school_age_share

    def classrooms_needed(self, population:float) -> int:
        """
        Classrooms for the whole school-age population, rounded up
        """
        return math.ceil(self.pupils(population) / self.__class_size)

    def additional_classrooms(self, current_population:float, future_population:float) -> int:
        """
        Extra classrooms needed, assuming current classrooms meet current need
        """
        return max(0, self.classrooms_needed(future_population) - self.classrooms_needed(current_population))
