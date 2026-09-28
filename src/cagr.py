import numpy
from .forecaster import Forecaster

""" 
Class for compound annual growth rate forecast
cagr = ((ending_population/starting_population)**(1/n))-1
"""
class Cagr(Forecaster):
    def fit(self, population:numpy.array):
            self.__population = population
            return self
    
    """ 
    override of abstract class' predict method 
    """
    def predict(self, horizon):
        last_value = self.__population[-1]
        first_value = self.__population[0]

        #apply formula, ((end_population/start_population)**1/length_of_data)-1
        cagr = ((last_value / first_value) ** (1 / len(self.__population))) - 1
        
        predictions = []
        for i in range(1, horizon + 1):
            value = last_value * (1 + cagr) ** i
            predictions.append(value)

        return numpy.array(predictions)
