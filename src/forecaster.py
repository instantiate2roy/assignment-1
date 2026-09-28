from abc import ABC, abstractmethod
import numpy

"""
base forecast class
"""
class Forecaster(ABC):
    """
    Absract method for fit
    """
    @abstractmethod
    def fit(self, population:numpy.array):
        pass

    """
    Abstract method for predict
    """        
    @abstractmethod
    def predict(self, horizon):
        pass