class FishStock:
    """class to do analysis of fish stock
        harvesting =  N(t+1) = N(t) + r·N(t)·(1 − N(t)/K) − h·N(t)
    """
    growth_rate = 0.4
    max_capacity = 10000
    start_capacity = 4000
    harvest_portion = 0.0 

    def weekly_growth(self, current_stock:float) -> float:
        """weeks growth"""
        return (self.growth_rate * current_stock) * (1- (current_stock/self.max_capacity))
        
    def weekly_catch(self, current_stock:int)->float:
        """ weeks harvest"""
        return self.harvest_portion*current_stock

    def increment(self, current_stock:float ):
        """increase in stock"""
        new_stock = current_stock + self.weekly_growth(current_stock) - self.weekly_catch(current_stock)
        return max(new_stock, 0.0)

    def simulate(self, weeks:int=1) ->dict:
        """ build dictionary of activity"""
        results = {}
        current_stock = self.start_capacity
        for week in range(1, weeks +1):
            next_stock = self.increment(current_stock)
            weekly_catch = self.weekly_catch(current_stock)
            weekly_growth = self.weekly_growth(current_stock)
            catch = weekly_catch
            if (current_stock + weekly_growth)<=weekly_catch:
                #catch can not exceed available fish
                catch = current_stock + weekly_growth
            
            results[week] = {'stock': current_stock,
                              'growth':weekly_growth,
                              'catch': catch,
                              'current_stock':next_stock
                              }
            current_stock = next_stock
        return results

    

    def generate_fibonacci_list(self, n: int, start: tuple[int, int] = (1, 1)) -> list[int]:
        """ Generate fibonacci Numbers as a list"""
        if n <= 0:
            return []
        seq = list(start[:n])
        while len(seq) < n:
            seq.append(seq[-1] + seq[-2])
        return seq
