import numpy
from scipy.signal import find_peaks

class Region:
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    def __init__(self, rain_fall:numpy.array, region:str  ,year:str = '2026') ->None:
        """ Initialize instance variables"""
        self.rain_fall_data = self.validate_rain_fall(rain_fall)
        self.region = self.validate_region(region)
        self.year = year

    @classmethod
    def validate_rain_fall(cls, rain_fall) -> numpy.ndarray:
        """
        Monthly rainfall must be 12 numbers (January to December), each finite and not negative
        """
        values = numpy.asarray(rain_fall)
        if values.ndim != 1 or len(values) != len(cls.months):
            raise ValueError(f"Rainfall needs exactly {len(cls.months)} values, one per month!")
        #integers and floats only: rejects text, None and True/False
        if values.dtype.kind not in 'iuf':
            raise ValueError("Rainfall values must be numbers!")
        if not numpy.all(numpy.isfinite(values)):
            raise ValueError("Rainfall values must be finite numbers!")
        if numpy.any(values < 0):
            raise ValueError("Rainfall cannot be negative!")
        return values

    @staticmethod
    def validate_region(region) -> str:
        """
        Region name must be a non-empty string
        """
        if not isinstance(region, str) or not region.strip():
            raise ValueError("Region name must be a non-empty string!")
        return region

    def __str__(self):
        print(self.region)

    def annual_total(self) -> float:    
        """
        Annual rainfall total
        """
        return float(numpy.sum(self.rain_fall_data))

    def mean(self)->float:
        """
        get mean of rain fall dist
        """
        return float(numpy.mean(self.rain_fall_data))

    def std(self) ->float:
        """
        Get the standard deviation
        """
        return numpy.std(self.rain_fall_data)
        
    def wettest_month(self) ->str:
        """
        wettest month
        """
        position_of_largest_val = numpy.argmax(self.rain_fall_data) 
        return self.months[position_of_largest_val]
        
    def driest_month(self) ->str:
        """
        Driest month
        """
        position_of_smallest_val = numpy.argmin(self.rain_fall_data) 
        return self.months[position_of_smallest_val]
        
    def co_efficient_of_variation(self):
        """
        co efficient of variation
        """
        #a region with no rain at all has no average to compare the spread with
        if self.mean() == 0:
            raise ValueError("Coefficient of variation is undefined when there is no rain!")
        return self.std()/self.mean()

    @staticmethod
    def pearson_correlation(a, b) -> float:
        """
        Pearson correlation between two vectors (-1 to 1).
        """
        a = numpy.asarray(a, dtype=float)
        b = numpy.asarray(b, dtype=float)
        if a.shape != b.shape:
            raise ValueError("Vectors must be the same length.")
        a_centred = a - a.mean()
        b_centred = b - b.mean()
        norm_a = numpy.linalg.norm(a_centred)
        norm_b = numpy.linalg.norm(b_centred)
        if norm_a == 0 or norm_b == 0:
            raise ValueError("Pearson correlation is undefined when a vector has no variation.")
        r = numpy.dot(a_centred, b_centred) / (norm_a * norm_b)
        return float(numpy.clip(r, -1.0, 1.0))
    
    @staticmethod
    def euclidean_distance(a, b) -> float:
        """
        Euclidean distance between two vectors (same units as the data).
        """
        a = numpy.asarray(a, dtype=float)
        b = numpy.asarray(b, dtype=float)
        if a.shape != b.shape:
            raise ValueError("Vectors must be the same length.")
        return float(numpy.linalg.norm(a - b))

    @staticmethod
    def cosine_similarity(a, b):
        """
        cosine similarity
        """
        a = numpy.asarray(a, dtype=float)
        b = numpy.asarray(b, dtype=float)
        norm_a = numpy.linalg.norm(a)
        norm_b = numpy.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            raise ValueError("Cosine similarity is undefined for a zero vector.")
        return numpy.dot(a, b) / (norm_a * norm_b)            
    
    @staticmethod
    def sine_similarity(a, b) -> float:
        """
        Sine of the angle between two vectors.
        """
        cos = Region.cosine_similarity(a, b)
        return float(numpy.sqrt(1.0 - cos**2))

    
    def rainy_seasons(self, min_prominence: float = 50) -> dict:
        """Detect rainy-season peaks and classify as unimodal or bimodal."""
        x = numpy.asarray(self.rain_fall_data, dtype=float)
        n = len(x)
        padded = numpy.concatenate([x, x, x])         # treat the year as circular
        idx, props = find_peaks(padded, prominence=min_prominence)
        keep = (idx >= n) & (idx < 2 * n)            # peaks in the middle copy only
        peaks = idx[keep] - n

        return {
            "region": self.region,
            "peak_months": [self.months[i] for i in peaks],
            "prominences": props["prominences"][keep].round().tolist(),
            "pattern": "bimodal" if len(peaks) >= 2 else "unimodal",
        }