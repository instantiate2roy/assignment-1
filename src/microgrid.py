import numpy
from src.matrix_equation import MatrixEquation

class MicroGrid():
    """
    Main MicroGrid class
    """
    
    def __init__(self):
        """ constructor to accept dependencies and define instance properties"""
        
        #These wont change irrespective of object
        self.co_efficients = [[3, 2],[4, 1]]
        self.__matrix_eqn = MatrixEquation(self.co_efficients)

    def determinant(self) -> float:
        """evaluate the determinant using the common matrix method"""
        return self.__matrix_eqn.determinant()
        
    def condition(self) -> float:
        """evaluate the condition  using the common matrix method"""
        return self.__matrix_eqn.condition()

    def solve_day(self, d1:float, d2:float):
         """ Solve the simultaneous equation  using the common matrix method"""
         return self.__matrix_eqn.solve(d1, d2)

        

