import copy
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
    """

    KG_PER_TONNE = 1000

    def __init__(self, fish_stock, price_model, n_paths: int = 1000, weeks: int = 52):
        self.fish_stock = fish_stock
        self.price_model = copy.copy(price_model)   # don't change the caller's seed
        self.n_paths = n_paths
        self.weeks = weeks

    def classify(self, cv: float) -> str:
        if cv <= 0.10:
            return "LOW"
        if cv <= 0.20:
            return "MODERATE"
        return "HIGH"

    def run(self) -> pandas.DataFrame:
        """Simulate n_paths price paths; one row per path (seed 0 to n_paths - 1)."""
        stock_data = self.fish_stock.simulate(self.weeks)   # same catch every path
        rows = []
        for seed in range(self.n_paths):
            self.price_model.seed = seed
            prices = self.price_model.simulate(self.weeks)
            revenue = [stock_data[week]["catch"] * self.KG_PER_TONNE * prices[week]
                       for week in stock_data]
            cv = statistics.stdev(revenue) / statistics.mean(revenue)
            rows.append({"annual_revenue": sum(revenue), "weekly_cv": cv})
        return pandas.DataFrame(rows)

    def value_at_risk(self, annual_revenue: pandas.Series, level: float = 0.05) -> float:
        """Annual revenue that is only undercut in `level` of years."""
        return float(numpy.percentile(annual_revenue, level * 100))