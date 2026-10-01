from .region import Region
import numpy

class CropRule(Region):
    crop_ranges = {'maize': [125,150], 'beans': [100,165], 'coffee':[135,200]}
    classification = ['Drought risk','Good for', "Waterlogging risk"]
    def __init__(self, rain_fall:numpy.array, region:str  ,year:int = '2026') ->None:
        """ Initialize instance variables"""
        super().__init__(rain_fall, region  ,year) 

    def classify(self):
        result = {}
        for month in range(0, len(self.months)):
            result[self.months[month]]= self.classification_by_crop(self.rain_fall_data[month])
            
        return result    
            

    def classification_by_crop(self, rain_value:float)->dict:
        
        result = {}
        for crop, rain_ranges in self.crop_ranges.items():
            
            if float(rain_value) < rain_ranges[0]:
                result[crop] = self.classification[0]
            elif float(rain_value) > rain_ranges[1]:
                result[crop] = self.classification[2]
            else:
                result[crop] = f"{self.classification[1]} {crop}"

        return result