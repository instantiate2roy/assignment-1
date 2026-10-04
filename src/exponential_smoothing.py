from forecaster import Forecaster
import numpy

class ExponentialSmoothing(Forecaster):
    """
    Simple exponential smoothing: level = alpha*y + (1-alpha)*previous level.
    """

    def __init__(self, alpha: float = 0.5):
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be between 0 (exclusive) and 1")
        self.alpha = alpha
        self._data = None
        self._levels = None

    def fit(self, population: numpy.array):
        data = numpy.asarray(population, dtype=float)
        if len(data) == 0:
            raise ValueError("Need at least 1 value to fit")
        levels = numpy.empty(len(data))
        levels[0] = data[0]
        for t in range(1, len(data)):
            levels[t] = self.alpha * data[t] + (1 - self.alpha) * levels[t - 1]
        self._data = data
        self._levels = levels
        return self

    def predict(self, horizon: int) -> numpy.array:
        if self._levels is None:
            raise RuntimeError("Call fit() before predict()")
        return numpy.full(horizon, self._levels[-1])

    def fitted(self) -> numpy.array:
        if self._levels is None:
            raise RuntimeError("Call fit() before fitted()")
        result = numpy.full(len(self._data), numpy.nan)
        result[1:] = self._levels[:-1]          # forecast for t uses the level at t-1
        return result
