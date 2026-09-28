import numpy
from .forecaster import Forecaster

class Linear(Forecaster):
    """ 
    Class for Linear/ straigh line gradient forecast
    formula is the equation of a straight line  "y=mx+b"
    """
    def fit(self, population:numpy.array):
        self.__population = population
        # apply expected fit formula y = mx + b, once, so predict() and fitted() share the same line
        self.__slope, self.__intercept = numpy.polyfit(numpy.arange(len(population)), population, 1)
        return self

    def predict(self, horizon) -> numpy.array:
        """ 
        override of abstract class' predict method 
        """
        future_x = numpy.arange(len(self.__population), len(self.__population) + horizon)
        return self.__slope * future_x + self.__intercept

    def fitted(self) -> numpy.array:
        """
        Values of the fitted line for the training years
        """
        x = numpy.arange(len(self.__population))
        return self.__slope * x + self.__intercept
