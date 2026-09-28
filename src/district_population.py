import numpy
import statistics
from .linear import Linear
from .fibonacci_ratio import FobonacciRatio
from .cagr import Cagr
from .validate import Validate

class DistrictPopulation:
    """ 
    Main class for District Population
    """
        
    def __init__(self, validate:Validate, years:numpy.ndarray, population:numpy.ndarray, district_name:str):
        """ 
        constructor to assign properties and inject dependencies 
        """
        self.__validate = validate
        self.__years = years
        #validate before assignment
        self.__validate.single_population(population)
        self.__validate.years_match_population(years, population)
        self.__population =  population
        self.__district_name = district_name

    def __len__(self) -> int:
        #get the number of years in the population sample
        return len(self.__population)

    def __repr__(self) -> str:
        return f"{self.__district_name} district"

    def mean(self, mode:str ='numpy') -> float:
        """
        Determine mean by either numpy or statistic module
        """
        match mode:
            case 'statistics':
                result = statistics.mean(self.__population.tolist()) 
            #default mode is numpy
            case 'numpy' | _:
                 result = numpy.mean(self.__population)
        return result          
    
    def median(self, mode:str ='numpy') -> float:
        """
        Determine median by either numpy or statistic module
        """
        match mode:
            case 'statistics':
                result = statistics.median(self.__population.tolist()) 
                    
            #default mode is numpy
            case 'numpy' | _:
                result = numpy.median(self.__population)
        return result     
    
    def variance(self, mode:str ='numpy') -> float:
        """
        Determine variance by either numpy (population, divides by N)
        or statistics module (sample, divides by N - 1)
        """
        match mode:
            case 'statistics': 
                result = statistics.variance(self.__population.tolist()) 
                            
            #default mode is numpy
            case 'numpy' | _:
                result =  numpy.var(self.__population)
        return result                
    
    def standard_deviation(self, mode:str ='numpy') -> float:
        """
        Determine std by either numpy (population, divides by N)
        or statistics module (sample, divides by N - 1), matching variance()
        """
        match mode:
            case 'statistics':
                result = statistics.stdev(self.__population.tolist()) 
                                    
            #default mode is numpy
            case 'numpy' | _:
                result = numpy.std(self.__population)
        return result
    
    def year_on_year_growth(self) -> dict:
        """ 
        compute anual growth
        """
        prev_year_value=0
        d = {}
        for i, p in enumerate(self.__population):
            #the first year has no previous year, and growth from 0 is undefined
            if i == 0 or prev_year_value == 0:
                d[str(self.__years[i])] = "N/A"
            else:
                d[str(self.__years[i])] = str(round(((p-prev_year_value)/prev_year_value)*100, 3))+'%'
            prev_year_value = p    
        return d

    def compound_annual_growth_rate(self) -> float:
        """
        compound annual growth rate 
        """
        #re-use method on Cagr class
        return Cagr().fit(self.__population).calculate()
        
    def __model(self, model:str):
        """
        Build and fit the chosen model on this district's population
        """
        match model:
            case 'Fibonacci':
                return FobonacciRatio().fit(self.__population)
            case 'Cagr':    
                return Cagr().fit(self.__population)
            case 'Linear'| _:
                return Linear().fit(self.__population)

    def prediction(self, horizon:int, model:str='Linear') -> numpy.ndarray:
        """ 
        Predicition method that allow switching between multiple models 
        """
        return self.__model(model).predict(horizon)

    def fitted(self, model:str='Linear') -> numpy.ndarray:
        """
        In-sample fitted values of the chosen model, one per year in this object
        """
        return self.__model(model).fitted()

    def __mae(self, predicted:numpy.ndarray,actual:numpy.ndarray) -> float:
        """ 
        MAE: mean absolute error, average error 
        """
        return numpy.mean(numpy.abs(actual - predicted))

    def __rmse(self, predicted:numpy.ndarray,actual:numpy.ndarray) -> float:
        """
        RMSE:Root mean square error 
        """
        return numpy.sqrt(numpy.mean((actual - predicted) ** 2))

    def __mape(self, predicted:numpy.ndarray,actual:numpy.ndarray) -> float:
        """
        MAPE:mean absolute percentage error, average error as a percentage
        """  
        return numpy.mean(numpy.abs((actual - predicted) / actual)) * 100

    def prediction_metrics(self, actual:numpy.ndarray, predicted:numpy.ndarray) -> dict:
        """ 
        Get all prediction metrics 
        """
        return {
            'MAE': round(self.__mae(predicted, actual),2),
            'RMSE': round(self.__rmse(predicted, actual),2),
            'MAPE': round(self.__mape(predicted, actual),2),
        }

    def best_model(self, predictions:dict) -> str:
        """
        Determine the best forecasting model based on MAE, RMSE, and MAPE.
        """
        metrics = {}
        for model, predicted in predictions.items():
            #skip actual, its not a real model
            if model == 'Actual-data':
                continue
            
            metrics[model] = predicted['metrics']
        
        # The model with the lowest value for each metric receives one point.
        scores = {model: 0 for model in metrics}
        for metric in ['MAE', 'RMSE', 'MAPE']:
            best = min(metrics,key=lambda model: metrics[model][metric])
            scores[best] += 1
        #The model with the highest total score is returned.
        return max(scores, key=scores.get)