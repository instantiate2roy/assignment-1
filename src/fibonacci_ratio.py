import numpy
from .forecaster import Forecaster

class FobonacciRatio(Forecaster):
    """ 
    Class for Fibonacci ratio forecast
        
        Formula: ratio  = Fn/Fn-1

        first entry/first fibonacci number
        second entry/second fibonacci number
        .
        .
        nth entry/nth fibonacci number   

        example 
            population = [1, 2, 3, 4, 5, 6..... nth] 
            fibonacci numbers = [1, 1, 2,3, 5, 8....nth]
        
        1/1 = 1.0
        2/1 = 2.0
        3/2 = 1.5
        4/3 = 1.333
        5/5 = 1
        6/8 = 0.75
        .
        .
        .
        nth/nth fibonacci number

    """
    
    def fit(self, population:numpy.array):
            self.__population = population
            return self

    def predict(self, horizon) -> numpy.array:
        """
        override of abstract class' predict method 
        """
        fibonacciList = self.__generateFibonacciNumbers(horizon)

        predictions = []
        last_value = self.__population[-1]

        for i in range(horizon):
            ratio = fibonacciList[i + 2] / fibonacciList[i + 1]
            predictions.append(last_value * ratio)

        return numpy.array(predictions)
    
    def __generateFibonacciNumbers(self, n:int) -> list:
        """ 
        Just a private method to help me generate fibonnaci numbers
        """    
        fibonacciList = [1, 1]
        for _ in range(n):
            fibonacciList.append(fibonacciList[-1] + fibonacciList[-2])
        return fibonacciList
