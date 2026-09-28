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

    def fitted(self) -> numpy.array:
        """
        In-sample values: what the model gives for the years it was fitted on.
        Not abstract, so models without a meaningful in-sample fit (Fibonacci) still work.
        """
        raise NotImplementedError(f"{type(self).__name__} has no fitted values")
