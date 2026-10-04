from .matrix_equation import MatrixEquation

class MicroGrid():
    """
    Main MicroGrid class
    """
    
    def __init__(self):
        """
        constructor to accept dependencies and define instance properties
        """
        self.co_efficients = [[3, 2],[4, 1]]
    
    def determinant(self) -> float:
        """evaluate the determinant using the common matrix method"""
        return MatrixEquation(self.co_efficients).determinant()
        
    def condition(self) -> float:
        """evaluate the condition  using the common matrix method"""
        return MatrixEquation(self.co_efficients).condition()

    def solve_day(self, d1:float, d2:float):
         """ Solve the simultaneous equation  using the common matrix method"""
         return MatrixEquation(self.co_efficients).solve(d1, d2)

        

