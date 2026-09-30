import copy
import math
import statistics

import numpy
import pandas


class RiskAssessor:
    """Classify revenue risk by CV and estimate 5% Value-at-Risk.

    Rule: a bad week (2 standard deviations below average) earns
    (1 - 2 x CV) of an average week.
        CV <= 10%  -> LOW       (bad week earns at least 80% of average)
        CV <= 20%  -> MODERATE  (bad week earns 60-80% of average)
        CV >  20%  -> HIGH      (bad week earns under 60% of average)
    With no catch there is no revenue, so the CV is undefined (NaN) and the class is N/A.
    """

    KG_PER_TONNE = 1000
    WEEKS_PER_YEAR = 52

    def __init__(self, fish_stock, price_model, n_paths: int = 1000, weeks: int = 52):
        self.fish_stock = fish_stock
        self.price_model = copy.copy(price_model)   # don't change the caller's seed
        self.n_paths = n_paths
        self.weeks = weeks

    def classify(self, cv: float) -> str:
        if math.isnan(cv):
            return "N/A"
        if cv <= 0.10:
            return "LOW"
        if cv <= 0.20:
            return "MODERATE"
        return "HIGH"

    def run(self) -> pandas.DataFrame:
        """Simulate n_paths price paths; one row per path (seed 0 to n_paths - 1).

        total_revenue covers all simulated weeks; annual_revenue is the average per 52-week year,
        so the two are equal when weeks = 52.
        """
        stock_data = self.fish_stock.simulate(self.weeks)   # same catch every path
        years = self.weeks / self.WEEKS_PER_YEAR
        rows = []
        for seed in range(self.n_paths):
            self.price_model.seed = seed
            prices = self.price_model.simulate(self.weeks)
            revenue = [stock_data[week]["catch"] * self.KG_PER_TONNE * prices[week]
                       for week in stock_data]
            mean_revenue = statistics.mean(revenue)
            #no catch means no revenue, and the CV is undefined rather than a division by zero
            cv = statistics.stdev(revenue) / mean_revenue if mean_revenue > 0 else float("nan")
            rows.append({"total_revenue": sum(revenue), "annual_revenue": sum(revenue) / years, "weekly_cv": cv})
        return pandas.DataFrame(rows)

    def value_at_risk(self, revenue: pandas.Series, level: float = 0.05) -> float:
        """Revenue that is only undercut in `level` of the simulated paths."""
        return float(numpy.percentile(revenue, level * 100))
