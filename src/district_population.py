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
        
    def __init__(self, validate:Validate, years:numpy.array, population:numpy.array, district_name:str):
        """ 
        constructor to assign properties and inject dependencies 
        """
        self.__validate = validate
        self.__years = years
        #validate before assignment
        self.__validate.single_population(population)
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
    
    def median(self, mode:str ='numpy') -> str:
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
    
    """
    Determine variance by either numpy or statistic module
    """
    def variance(self, mode:str ='numpy'):
        match mode:
            case 'statistics': 
                result = statistics.variance(self.__population.tolist()) 
                            
            #default mode is numpy
            case 'numpy' | _:
                result =  numpy.var(self.__population)
        return result                
    
    def standard_deviation(self, mode:str ='numpy') -> float:
        """
        Determine std by either numpy or statistic module
        """
        match mode:
            case 'statistics':
                result = statistics.pstdev(self.__population.tolist()) 
                                    
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
            if i ==0:
                d[str(self.__years[i])] = "0.0%"
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
        
    def prediction(self, horizon:int, model:str='Linear') -> numpy.array:
        """ 
        Predicition method that allow switching between multiple models 
        """
        match model:
            case 'Fibonacci':
                model = FobonacciRatio().fit(self.__population)
            case 'Cagr':    
                model = Cagr().fit(self.__population)
            case 'Linear'| _:
                model = Linear().fit(self.__population)

        return model.predict(horizon)        

    def __mae(self, predicted:numpy.array,actual:numpy.array) -> float:
        """ 
        MAE: mean absolute error, average error 
        """
        return numpy.mean(numpy.abs(actual - predicted))

    def __rmse(self, predicted:numpy.array,actual:numpy.array) -> float:
        """
        RMSE:Root mean square error 
        """
        return numpy.sqrt(numpy.mean((actual - predicted) ** 2))

    def __mape(self, predicted:numpy.array,actual:numpy.array) -> float:
        """
        MAPE:mean absolute percentage error, average error as a percentage
        """  
        return numpy.mean(numpy.abs((actual - predicted) / actual)) * 100

    def prediction_metrics(self, actual:numpy.array, predicted:numpy.array) -> dict:
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

    def prediction(self, horizon:int, model:str='Linear') -> numpy.array:
        """ 
        Predicition method that allow switching between multiple models 
        """
        return self.__model(model).predict(horizon)

    def fitted(self, model:str='Linear') -> numpy.array:
        """
        In-sample fitted values of the chosen model, one per year in this object
        """
        return self.__model(model).fitted()    
