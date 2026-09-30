import numpy

class PriceModel:
    """Weekly fish price in UGX/kg as a seeded, bounded random walk."""

    start_price = 12000
    upper_limit = 16000
    lower_limit = 9000
    step_sd = 300     
    seed =50         

    def simulate(self, weeks: int = 52) -> dict[int, float]:
        """Return {week: price} for weeks 1 to `weeks`."""
        rng = numpy.random.default_rng(self.seed)
        prices = []
        price = self.start_price

        for week in range(1, weeks + 1):
            prices.append(price)
            step = round(rng.normal(0, self.step_sd) / 10) * 10
            price = min(max(price + step, self.lower_limit), self.upper_limit)

        week_numbers = range(1, weeks + 1)
        return dict(zip(week_numbers, prices))
 