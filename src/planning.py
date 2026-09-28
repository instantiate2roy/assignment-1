import math
import numbers


class ClassroomPlanner:
    """
    Estimate primary-school classrooms from population figures.
    """

    def __init__(self, school_age_share:float = 0.18, class_size:int = 53, population_unit:float = 1):
        """
        Args:
            school_age_share: Share of the population of primary-school age (0.18 = 18%).
            class_size: Pupils one classroom holds.
            population_unit: Multiplier to get headcount, e.g. 1000 if the data is in thousands.
        """
        if not self.__is_number(school_age_share) or not 0 < school_age_share <= 1:
            raise ValueError("School-age share must be a number greater than 0 and at most 1!")
        if isinstance(class_size, bool) or not isinstance(class_size, numbers.Integral) or class_size <= 0:
            raise ValueError("Class size must be a whole number greater than 0!")
        if not self.__is_number(population_unit) or population_unit <= 0:
            raise ValueError("Population unit must be a number greater than 0!")
        self.__school_age_share = school_age_share
        self.__class_size = class_size
        self.__population_unit = population_unit

    @staticmethod
    def __is_number(value) -> bool:
        """
        True for a finite int or float (numpy numbers included).
        False for bools, strings, None, NaN and infinity.
        """
        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            return False
        return math.isfinite(value)

    def __validate_population(self, population) -> None:
        """
        A population must be a finite number and cannot be negative
        """
        if not self.__is_number(population):
            raise ValueError("A Population entry must be a finite number!")
        if population < 0:
            raise ValueError("A Population entry cannot be a negative value!")

    def pupils(self, population:float) -> float:
        """
        Number of primary-school-age children in a population
        """
        self.__validate_population(population)
        return population * self.__population_unit * self.__school_age_share

    def classrooms_needed(self, population:float) -> int:
        """
        Classrooms for the whole school-age population, rounded up
        """
        return math.ceil(self.pupils(population) / self.__class_size)

    def additional_classrooms(self, current_population:float, future_population:float) -> int:
        """
        Extra classrooms needed, assuming current classrooms meet current need exactly.
        Returns 0 when the population shrinks, since no new classrooms are needed.
        """
        return max(0, self.classrooms_needed(future_population) - self.classrooms_needed(current_population))
