import numpy

from .microgrid import MicroGrid


class SensitivityAnalysis:
    """
    Monte Carlo sensitivity of a MicroGrid's solar (x) and battery (y) dispatch to errors in D1 and D2
    """

    def __init__(self, grid:MicroGrid, n_draws:int = 1000, spread:float = 0.05, seed:int = 42):
        """
        Args:
            grid: The 2x2 MicroGrid to test.
            n_draws: Number of Monte Carlo draws.
            spread: Largest relative error in each demand reading (0.05 = +/-5%).
            seed: Seed for numpy's random generator, so every run draws the same errors.
        """
        if isinstance(n_draws, bool) or not isinstance(n_draws, int) or n_draws <= 0:
            raise ValueError("Number of draws must be a whole number greater than 0!")
        if not 0 < spread < 1:
            raise ValueError("Spread must be greater than 0 and less than 1!")
        self.__grid = grid
        self.__n_draws = n_draws
        self.__spread = spread
        self.__seed = seed

    def perturbed_demands(self, d1:float, d2:float) -> numpy.ndarray:
        """
        One row per draw: D1 and D2 each multiplied by an independent uniform factor in [1 - spread, 1 + spread]
        """
        rng = numpy.random.default_rng(self.__seed)
        factors = rng.uniform(1 - self.__spread, 1 + self.__spread, size=(self.__n_draws, 2))
        return numpy.array([d1, d2]) * factors

    def run(self, d1:float, d2:float) -> tuple[numpy.ndarray, numpy.ndarray]:
        """
        Solve every perturbed day. Returns the perturbed demands and the matching x, y dispatch, one row per draw.
        """
        demands = self.perturbed_demands(d1, d2)
        dispatch = numpy.array([self.__grid.solve_day(a, b) for a, b in demands])
        return demands, dispatch

    def amplification(self, d1:float, d2:float) -> numpy.ndarray:
        """
        For each draw, the relative change in the dispatch divided by the relative change in the demand (2-norms).
        The condition number is the largest value this can ever take.
        """
        base_demand = numpy.array([d1, d2])
        base_dispatch = self.__grid.solve_day(d1, d2)
        demands, dispatch = self.run(d1, d2)

        demand_change = numpy.linalg.norm(demands - base_demand, axis=1) / numpy.linalg.norm(base_demand)
        dispatch_change = numpy.linalg.norm(dispatch - base_dispatch, axis=1) / numpy.linalg.norm(base_dispatch)
        return dispatch_change / demand_change
