import numpy

class MicroGrid():
    """
    Main MicroGrid class
    """
    
    def __init__(self):
        """ constructor to accept dependencies and define instance properties"""
        #These wont change irrespective of object
        self.co_efficients = [[3, 2],[4, 1]]

    def determinant(self) -> float:
        """evaluate the determinant"""
        det = numpy.linalg.det(self.co_efficients)
        #determinant can not be 0, 
        if abs(det) < 1e-10:
            raise ValueError('Invalid Co-efficient combination!')
        return det

    def condition(self) -> float:
        """evaluate the condition"""
        return numpy.linalg.cond(self.co_efficients)    

    def solve_day(self, d1:float, d2:float):
         """ Solve the simultaneous equation"""
         return numpy.linalg.solve(self.co_efficients, numpy.array([d1, d2]))

        

