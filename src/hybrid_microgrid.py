import numpy

from .microgrid import MicroGrid


class HybridMicroGrid(MicroGrid):
    """
    MicroGrid with a diesel generator (z) as a third source and a night-time load as a third constraint:

        3x + 2y +  z = D1    daytime load
        4x +  y + 2z = D2    critical-equipment load
        0x + 2y + 3z = D3    night-time load (no solar at night)

    determinant() and condition() are inherited and work on the 3x3 matrix unchanged.
    """

    def __init__(self, night_row:list[float] = None):
        """
        Args:
            night_row: Coefficients of x, y and z in the third equation. Defaults to [0, 2, 3].
                Passing a row that depends on the first two, such as their sum [7, 3, 3],
                shows what happens when the system has no unique solution.
        """
        super().__init__()
        night_row = [0, 2, 3] if night_row is None else list(night_row)
        if len(night_row) != 3:
            raise ValueError("The night-time equation needs exactly 3 coefficients (x, y, z)!")

        #keep the parent's two equations and add diesel's share of each load (1 and 2)
        diesel = [1, 2]
        self.co_efficients = [row + [z] for row, z in zip(self.co_efficients, diesel)] + [night_row]

    def solve_day(self, d1:float, d2:float, d3:float) -> numpy.ndarray:
        """
        Solve for solar (x), battery (y) and diesel (z).
        Raises ValueError, through the inherited determinant check, when there is no unique solution.
        """
        self.determinant()
        return numpy.linalg.solve(self.co_efficients, numpy.array([d1, d2, d3]))

    def rank(self) -> int:
        """
        Number of independent equations: 3 for a unique solution, fewer when one equation depends on the others
        """
        return int(numpy.linalg.matrix_rank(self.co_efficients))

    def solution_count(self, d1:float, d2:float, d3:float) -> str:
        """
        'one' when the equations are independent. When they are not, 'infinitely many' if the demands
        follow the same dependence as the equations, otherwise 'none'.
        """
        coefficients = numpy.array(self.co_efficients, dtype=float)
        if self.rank() == 3:
            return 'one'
        #adding the demands as a column raises the rank only when they contradict the dependence
        extended = numpy.column_stack([coefficients, [d1, d2, d3]])
        return 'infinitely many' if numpy.linalg.matrix_rank(extended) == self.rank() else 'none'
