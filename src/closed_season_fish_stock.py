from fish_stock import FishStock

class ClosedSeasonFishStock(FishStock):
    """FishStock with no harvesting during a closed season each year."""

    closed_weeks = range(1, 9)   # weeks 1-8 of every year
    weeks_per_year = 52

    def is_closed(self, week: int) -> bool:
        week_of_year = (week - 1) % self.weeks_per_year + 1
        return week_of_year in self.closed_weeks

    def simulate(self, weeks: int = 52) -> dict:
        results = {}
        current_stock = self.start_capacity
        for week in range(1, weeks + 1):
            growth = self.weekly_growth(current_stock)
            if self.is_closed(week):
                catch = 0.0
            else:
                catch = min(self.weekly_catch(current_stock), current_stock + growth)
            next_stock = max(current_stock + growth - catch, 0.0)
            results[week] = {'stock': current_stock, 'growth': growth,
                             'catch': catch, 'current_stock': next_stock}
            current_stock = next_stock
        return results