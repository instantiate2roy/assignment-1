import numpy
from .forecaster import Forecaster

class Linear(Forecaster):
    """ 
    Class for Linear/ straigh line gradient forecast
    formula is the equation of a straight line  "y=mx+b"
    """
    def fit(self, population:numpy.array):
            self.__population = population
            return self

    
    def predict(self, horizon) -> numpy.array:
        """ 
        override of abstract class' predict method 
        """
        
        # apply expected fit formula y = mx + b
        slope, intercept = numpy.polyfit(numpy.arange(len(self.__population)), self.__population, 1)
        future_x = numpy.arange(len(self.__population),len(self.__population) + horizon)
        return slope * future_x + intercept
