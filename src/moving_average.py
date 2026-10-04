from forecaster import Forecaster
import numpy

class MovingAverage(Forecaster):
    """
    Forecast each step as the mean of the previous `window` values.
    """

    def __init__(self, window: int = 3):
        if window < 1:
            raise ValueError("window must be at least 1")
        self.window = window
        self._data = None

    def fit(self, population: numpy.array):
        data = numpy.asarray(population, dtype=float)
        if len(data) < self.window:
            raise ValueError(f"Need at least {self.window} values to fit")
        self._data = data
        return self

    def predict(self, horizon: int) -> numpy.array:
        if self._data is None:
            raise RuntimeError("Call fit() before predict()")
        history = list(self._data)
        forecasts = []
        for _ in range(horizon):
            next_value = numpy.mean(history[-self.window:])
            forecasts.append(next_value)
            history.append(next_value)          # roll forward using the forecast
        return numpy.array(forecasts)

    def fitted(self) -> numpy.array:
        if self._data is None:
            raise RuntimeError("Call fit() before fitted()")
        result = numpy.full(len(self._data), numpy.nan)
        for t in range(self.window, len(self._data)):
            result[t] = self._data[t - self.window:t].mean()
        return result