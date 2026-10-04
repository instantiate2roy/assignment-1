import numpy

class MatrixEquation():
    """
    Matrice class class
    """
    
    def __init__(self, co_efficients):
        """ 
        constructor to accept dependencies and define instance variables
        """
        self.co_efficients = co_efficients

    def determinant(self) -> float:
        """
        evaluate the determinant
        """
        det = numpy.linalg.det(self.co_efficients)
        #determinant can not be 0, 
        if abs(det) < 1e-10:
            raise ValueError('Invalid Co-efficient combination!')
        return det

    def condition(self) -> float:
        """
        evaluate the condition"""
        return numpy.linalg.cond(self.co_efficients)    

    def solve(self, value1:float, value2:float):
         """
         Solve the simultaneous equation
         """
         return numpy.linalg.solve(self.co_efficients, numpy.array([value1, value2]))

        

