import math
import numbers

from .region import Region
import numpy

class CropRule(Region):
    crop_ranges = {'maize': [125,150], 'beans': [100,165], 'coffee':[135,200]}
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    classification = ['Drought risk','Good for', "Waterlogging risk"]

    def __init__(self, rain_fall:numpy.array, region:str  ,year:int = '2026') ->None:
        """ Initialize instance variables"""
        self.rain_fall_data = self.validate_rain_fall(rain_fall)
        self.region = self.validate_region(region)
        self.year = year

    def classify(self):
        result = {}
        for month in range(0, len(self.months)):
            result[self.months[month]]= self.classification_by_crop(self.rain_fall_data[month])
            
        return result    
            

    def classification_by_crop(self, rain_value:float)->dict:
        """ Classify one month's rainfall (mm) for every crop"""
        if isinstance(rain_value, bool) or not isinstance(rain_value, numbers.Real) or not math.isfinite(rain_value):
            raise ValueError("Rainfall must be a number!")
        if rain_value < 0:
            raise ValueError("Rainfall cannot be negative!")

        result = {}
        for crop, rain_ranges in self.crop_ranges.items():
            
            if float(rain_value) < rain_ranges[0]:
                result[crop] = self.classification[0]
            elif float(rain_value) > rain_ranges[1]:
                result[crop] = self.classification[2]
            else:
                result[crop] = f"{self.classification[1]} {crop}"

        return result