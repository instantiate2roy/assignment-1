import numpy
import pytest

from src.microgrid import MicroGrid
from src.sensitivity import SensitivityAnalysis


@pytest.fixture
def analysis():
    return SensitivityAnalysis(MicroGrid(), n_draws=1000, spread=0.05, seed=42)


def test_demands_stay_within_the_spread(analysis):
    demands = analysis.perturbed_demands(100, 70)
    assert demands.shape == (1000, 2)
    assert numpy.all(demands >= [95, 66.5]) and numpy.all(demands <= [105, 73.5])


def test_same_seed_gives_the_same_draws(analysis):
    again = SensitivityAnalysis(MicroGrid(), seed=42)
    other = SensitivityAnalysis(MicroGrid(), seed=7)
    assert numpy.array_equal(analysis.perturbed_demands(100, 70), again.perturbed_demands(100, 70))
    assert not numpy.array_equal(analysis.perturbed_demands(100, 70), other.perturbed_demands(100, 70))


def test_every_draw_is_solved(analysis):
    grid = MicroGrid()
    demands, dispatch = analysis.run(100, 70)
    for (d1, d2), expected in zip(demands[:5], dispatch[:5]):
        assert grid.solve_day(d1, d2) == pytest.approx(expected)


def test_amplification_never_exceeds_the_condition_number(analysis):
    # ||dx|| / ||x|| <= cond(A) * ||db|| / ||b|| for every possible error, so it must hold for every draw
    amplification = analysis.amplification(100, 70)
    assert numpy.all(amplification <= MicroGrid().condition() + 1e-9)
    assert amplification.max() > 1


def test_equal_errors_in_both_demands_scale_the_dispatch_equally():
    # The system is linear, so +5% on D1 and D2 together is +5% on x and y, an amplification of exactly 1
    grid = MicroGrid()
    assert grid.solve_day(105, 73.5) == pytest.approx(grid.solve_day(100, 70) * 1.05)


@pytest.mark.parametrize('settings', [
    {'n_draws': 0},
    {'n_draws': 10.5},
    {'n_draws': True},
    {'spread': 0},
    {'spread': 1},
    {'spread': -0.05},
])
def test_invalid_settings_are_rejected(settings):
    with pytest.raises(ValueError):
        SensitivityAnalysis(MicroGrid(), **settings)
