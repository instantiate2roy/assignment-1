import numpy

class MicroGrid():
    """
    Main MicroGrid class
    """
    #These wont change irrespective of object
    co_efficients = [[3, 2],[4, 1]]

    def determinant(self) -> int:
        """evaluate the determinant"""
        det = numpy.linalg.det(self.co_efficients)
        #determinant can not be 0, 
        if abs(det) < 1e-10:
            raise ValueError('Invalid Co-efficient combination!')
        return det

    def condition(self) -> float:
        """evaluate the condition"""
        return numpy.linalg.cond(self.co_efficients)    

    def solve(self, d1:float, d2:float):
         """ Solve the simultaneous equation"""
         return numpy.linalg.solve(self.co_efficients, numpy.array([d1, d2]))

        

