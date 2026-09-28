import numpy
from .forecaster import Forecaster


class Cagr(Forecaster):
    """ 
    Class for compound annual growth rate forecast
    cagr = ((ending_population/starting_population)**(1/n))-1
    """        
    def fit(self, population:numpy.array):
            self.__population = population
            return self
    
    def predict(self, horizon) -> numpy.array:
        """ 
        override of abstract class' predict method 
        """
        
        cagr = self.calculate()
        
        predictions = []
        for i in range(1, horizon + 1):
            value = self.__population[-1] * (1 + cagr) ** i
            predictions.append(value)

        return numpy.array(predictions)

    def calculate(self) -> float:
        """
        calculate cagr
        """   
        #apply formula, ((end_population/start_population)**1/length_of_data-1)-1  
        return ((self.__population[-1] / self.__population[0]) ** (1 / (len(self.__population) - 1))) - 1

    def fitted(self) -> numpy.array:
        """
        Growth curve from the first value at the CAGR rate, for the training years.
        It ends exactly on the last training value, because that is how the rate is defined.
        """
        cagr = self.calculate()
        return self.__population[0] * (1 + cagr) ** numpy.arange(len(self.__population))
