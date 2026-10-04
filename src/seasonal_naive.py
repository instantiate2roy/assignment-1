import numpy
from .forecaster import Forecaster

class SeasonalNaive(Forecaster):
    """
    Forecast each day as the value from the same day one season earlier
    (with season=7: next Friday = last Friday).
    """

    def __init__(self, season: int = 7):
        if season < 1:
            raise ValueError("season must be at least 1")
        self.season = season
        self._data = None

    def fit(self, population: numpy.array):
        data = numpy.asarray(population, dtype=float)
        if len(data) < self.season:
            raise ValueError(f"Need at least {self.season} values to fit")
        self._data = data
        return self

    def predict(self, horizon: int) -> numpy.array:
        if self._data is None:
            raise RuntimeError("Call fit() before predict()")
        last_season = self._data[-self.season:]
        return numpy.array([last_season[h % self.season] for h in range(horizon)])

    def fitted(self) -> numpy.array:
        if self._data is None:
            raise RuntimeError("Call fit() before fitted()")
        result = numpy.full(len(self._data), numpy.nan)
        result[self.season:] = self._data[:-self.season]
        return result