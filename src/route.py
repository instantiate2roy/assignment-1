import numpy
import statistics

class Route:
    def __init__(self,route:str, passenger_counts:numpy.array, fare:int):
        self.__route = route
        self.__passenger_counts= passenger_counts
        self.__fare = fare

    def daily_revenue(self) ->numpy.array:
        """
        Get daily revenues
        """
        day_revenues = []
        for day_count in self.__passenger_counts:
            day_revenues.append(self.__fare*day_count)
        return numpy.array(day_revenues)

    def total_revenue(self) -> float:
        """
        Get total revenue over 10 days
        """
        return numpy.sum(self.__passenger_counts)*self.__fare

    def mean(self) -> float:
        """
        Average revenue per day
        """
        return statistics.mean(self.daily_revenue().tolist())

    def variance(self) -> float:
        """
        variance of daily revenue
        """
        return statistics.variance(self.daily_revenue().tolist())

    def std(self) -> float:
        """
        standard deviation of daily revenue
        """
        return statistics.stdev(self.daily_revenue().tolist())

