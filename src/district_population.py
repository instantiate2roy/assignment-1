import numpy
import statistics
from .linear import Linear
from .fibonacci_ratio import FobonacciRatio
from .cagr import Cagr

""" 
Main class for District Population
"""
class DistrictPopulation:
    
    """ 
    constructor to assign properties and inject dependencies 
    """
    def __init__(self, years:numpy.array, population:numpy.array, district_name:str):
        self.__years = years
        self.__population =  population
        self.__district_name = district_name

    def __len__(self):
        #get the number of years in the population sample
        return len(self.__population)

    def __repr__(self):
        return f"{self.__district_name} district"

    """
    Determine mean by either numpy or statistic module
    """
    def mean(self, mode:str ='numpy'):
        match mode:
            case 'statistics':
                result = statistics.mean(self.__population) 
            #default mode is numpy
            case 'numpy' | _:
                 result = numpy.mean(self.__population)
        return result          
    
    """
    Determine median by either numpy or statistic module
    """
    def median(self, mode:str ='numpy'):
        match mode:
            case 'statistics':
                result = statistics.median(self.__population) 
                    
            #default mode is numpy
            case 'numpy' | _:
                result = numpy.median(self.__population)
        return result     
    
    """
    Determine variance by either numpy or statistic module
    """
    def variance(self, mode:str ='numpy'):
        match mode:
            case 'statistics': 
                result = statistics.variance(self.__population) 
                            
            #default mode is numpy
            case 'numpy' | _:
                result =  numpy.var(self.__population)
        return result                
    
    """
    Determine std by either numpy or statistic module
    """
    def standard_deviation(self, mode:str ='numpy'):
        match mode:
            case 'statistics':
                result = statistics.pstdev(self.__population) 
                                    
            #default mode is numpy
            case 'numpy' | _:
                result = numpy.std(self.__population)
        return result
    
    """ 
    computer anual growth
    """
    def year_on_year_growth(self):
        prev_year_value=0
        d = {}
        for i, p in enumerate(self.__population):
            if i ==0:
                d[str(self.__years[i])] = "0.0%"
            else:
                d[str(self.__years[i])] = str(round(((p-prev_year_value)/prev_year_value)*100, 3))+'%'
            prev_year_value = p    
        return d

    """ 
    compound annual growth rate 
    """
    def compound_annual_growth_rate(self):
        return ((self.__population[-1] / self.__population[0]) ** (1 / len(self.__years))) - 1

    """ 
    Predicition method that allow switching between multiple models 
    """
    def prediction(self, horizon:int, model:str='Linear'):
        match model:
            case 'Fibonacci':
                model = FobonacciRatio().fit(self.__population)
            case 'Cagr':    
                model = Cagr().fit(self.__population)
            case 'Linear'| _:
                model = Linear().fit(self.__population)

        return model.predict(horizon)        

    """ 
    mean absolute error, average error 
    """
    def __mae(self, predicted:numpy.array,actual:numpy.array):
        return numpy.mean(numpy.abs(actual - predicted))

    """
    Root mean square error 
    """    
    def __rmse(self, predicted:numpy.array,actual:numpy.array):
        return numpy.sqrt(numpy.mean((actual - predicted) ** 2))

    """
    mean absolute percentage error, average error as a percentage
    """        
    def __mape(self, predicted:numpy.array,actual:numpy.array):
        return numpy.mean(numpy.abs((actual - predicted) / actual)) * 100

    """ 
    Get all prediction metrics 
    """
    def prediction_metrics(self, actual:numpy.array, predicted:numpy.array):
        return {
            'MAE': round(self.__mae(predicted, actual),2),
            'RMSE': round(self.__rmse(predicted, actual),2),
            'MAPE': round(self.__mape(predicted, actual),2),
        }

    """
    Determine the best forecasting model based on MAE, RMSE, and MAPE.
    """
    def best_model(self, predictions:dict):
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
