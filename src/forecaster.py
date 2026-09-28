from abc import ABC, abstractmethod
import numpy

class Forecaster(ABC):
    """
    base forecast class
    """
    
    @abstractmethod
    def fit(self, population:numpy.array):
        """
        Absract method for fit
        """
        pass

    @abstractmethod
    def predict(self, horizon) -> numpy.array:
        """
        Abstract method for predict
        """         
        pass