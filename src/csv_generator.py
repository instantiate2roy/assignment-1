import csv
import random

class CsvGenerator:
    """
    Generte CSV files
    """

    def solar_grid_csv(self, file_name_and_path:str, n_days:int = 30,seed_number :int = 30, all_feasible = True):
        """Generate csv file of predictable data"""

        #data needs to be somewhat predictable, hence seed number
        random.seed(seed_number)
        
        #Note: file will be overwritten if exists
        with open(file_name_and_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["day", "d1", "d2"])
            
            #n days worth of data
            for day in range(1, n_days+1):
                weekday = (day - 1) % 7
                d1, d2 = self.__generate_day_data_pattern(weekday, day ,all_feasible)
                writer.writerow([day,round(d1, 2),round(d2, 2)])

    def __generate_day_data_pattern(self, weekday: int, day:int, all_feasible:bool = True) -> list:
        """try to fake a pattern, add feasibility check to gen bad data """
        #Define pattern, so on a given weekday the data is somewhat similar
        if weekday in [5, 6]:
            d1 = 80
            d2 = 50
        else:
            d1 = 100
            d2 = 70
        d1, d2 = self.__add_noise(d1, d2)

        #break some days after the noise, so the noise can't undo it
        if not all_feasible:
            if day % 10 == 0:
                if day % 20 == 0:
                    d2 = d1 * 0.4    #negative solar (x)
                else:
                    d2 = d1 * 1.5    #negative battery (y)

            #make days 5, 15, 25 have negative meter readings
            if day % 10 == 5:
                if day % 20 == 5:
                    d1 = -d1
                else:
                    d2 = -d2

        return [d1, d2]

    def __add_noise(self, d1 , d2)->list:
        """Add noise to data"""
        return [d1 + random.uniform(-10, 10), d2 + random.uniform(-7, 7)]


