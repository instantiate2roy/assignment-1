import pytest

from src.hybrid_microgrid import HybridMicroGrid
from src.microgrid import MicroGrid


@pytest.fixture
def hybrid():
    return HybridMicroGrid()


def test_hybrid_extends_the_two_source_grid(hybrid):
    assert isinstance(hybrid, MicroGrid)
    assert hybrid.co_efficients == [[3, 2, 1], [4, 1, 2], [0, 2, 3]]


def test_inherited_determinant_works_on_three_equations(hybrid):
    # det = 3(1*3 - 2*2) - 2(4*3 - 2*0) + 1(4*2 - 1*0) = -3 - 24 + 8 = -19
    assert hybrid.determinant() == pytest.approx(-19)
    assert hybrid.rank() == 3


def test_solve_day_matches_hand_calculation(hybrid):
    # x = 10, y = 20, z = 5 gives D1 = 30 + 40 + 5, D2 = 40 + 20 + 10, D3 = 40 + 15
    assert hybrid.solve_day(75, 70, 55) == pytest.approx([10, 20, 5])
    assert hybrid.solution_count(75, 70, 55) == 'one'


# Edge cases: a third equation that depends on the first two

@pytest.fixture
def dependent():
    # The night-time row is the sum of the other two rows
    return HybridMicroGrid(night_row=[7, 3, 3])


def test_dependent_equation_leaves_no_unique_solution(dependent):
    assert dependent.rank() == 2
    with pytest.raises(ValueError):
        dependent.solve_day(100, 70, 170)


def test_dependent_equation_gives_infinitely_many_or_no_solutions(dependent):
    # D3 = D1 + D2 follows the same dependence as the rows; any other D3 contradicts it
    assert dependent.solution_count(100, 70, 170) == 'infinitely many'
    assert dependent.solution_count(100, 70, 150) == 'none'


def test_nearly_dependent_equation_is_badly_conditioned():
    near = HybridMicroGrid(night_row=[7, 3, 3.01])
    assert near.condition() > 1000
    # A 1% change in D3 moves solar from 8 kWh to -94 kWh
    assert near.solve_day(100, 70, 170)[0] == pytest.approx(8)
    assert near.solve_day(100, 70, 171.7)[0] == pytest.approx(-94)


def test_night_row_needs_three_coefficients():
    with pytest.raises(ValueError):
        HybridMicroGrid(night_row=[1, 2])
