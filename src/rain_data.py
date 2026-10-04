import requests
import csv
import numpy

class RainData:
    """Class to import rain data"""
    #NASA POWER uri
    base_url = 'https://power.larc.nasa.gov/api/temporal/monthly/point'
    base_file_dir = './files'

    def __init__(self, location:str, cordinates:dict):
        """constructor"""
        self.__location = location
        self.__cordinates = cordinates
        self.__file_location = f"{self.base_file_dir}/{self.__location}_rain_data.csv"

    def get(self):
        """
        Load rain data
        - Take from Live API call
        - When API call fails default to file read
        """
        reqeuest_parameter = {
                "parameters": "PRECTOTCORR_SUM",   # monthly rainfall total in mm
                "community": "AG",
                "longitude": self.__cordinates["lon"],
                "latitude": self.__cordinates["lat"],
                "start": "2016",
                "end": "2025", 
                "format": "JSON",
            }
        
        try:
            response = requests.get(self.base_url, params=reqeuest_parameter, timeout=60)
            response.raise_for_status()
            data = response.json()["properties"]["parameter"]["PRECTOTCORR_SUM"]
            
            self.__save_to_file(data)
        except requests.RequestException as e:
            #If http request fail, attemp to load data from old files 
            print(f"Failed to fetch data for {self.__location}: {e}")
            if not self.__file_location.exists():
                raise FileNotFoundError(f"No saved data for {self.__location} at {self.__file_location}")
        
        print("Loading from Files..........")
        return self.__load_from_file()
            

    def __save_to_file(self, data):
        """
        Write to csv file
        """
        with open(self.__file_location, "w") as f:
            #write header
            f.write("year,month,rainfall_mm\n") 
            for key, value in data.items():
                #Annual total record, skip it
                if key.endswith("13"):
                    continue

                year, month = key[:4], key[4:]
                #Handle empty values
                rain = "" if value == -999 else value  
                f.write(f"{year},{month},{rain}\n")

    def __load_from_file(self) -> dict:
        """
        Read the csv file into {year: numpy array of 12 values}.
        """
        by_year = {}
        with open(self.__file_location, "r") as f:
            for row in csv.DictReader(f):
                rain = float(row["rainfall_mm"]) if row["rainfall_mm"] else numpy.nan
                by_year.setdefault(int(row["year"]), []).append(rain)
        return {year: numpy.array(values) for year, values in by_year.items()}


            
        