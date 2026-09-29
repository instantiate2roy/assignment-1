import csv
import random

class CsvGenerator:
    """
    Generte CSV files
    """

    def solar_grid_csv(self, file_name_and_path:str, n_days:int = 30,seed_number :int = 30):
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
                d1, d2 = self.__generate_day_data_pattern(weekday)

                writer.writerow([
                    day,
                    round(d1, 2),
                    round(d2, 2)
                ])

    def __generate_day_data_pattern(self, weekday: int) -> list:
        """try to fake a pattern """
        #Define pattern, so on a give weekday the data is somewhat similar
        if weekday in [5, 6]:
            a = 80
            b = 50
        else:                      
            a = 100
            b = 70
        return self.__add_noise(a, b)   

    def __add_noise(self, d1 , d2)->list:
        """Add noise to data"""
        return [d1 + random.uniform(-10, 10), d2 + random.uniform(-7, 7)]


