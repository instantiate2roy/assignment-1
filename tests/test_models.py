import numpy
import pytest

from src.cagr import Cagr
from src.fibonacci_ratio import FobonacciRatio
from src.linear import Linear


def test_cagr_uses_periods_not_data_points():
    # 3 values = 2 periods of 10% growth, so the rate must be 0.10, not 121/100 ** (1/3) - 1
    assert Cagr().fit(numpy.array([100, 110, 121])).calculate() == pytest.approx(0.10)


def test_cagr_predict_grows_from_last_value():
    forecast = Cagr().fit(numpy.array([100, 110, 121])).predict(2)
    assert forecast == pytest.approx([133.1, 146.41])


def test_cagr_fitted_ends_on_last_value():
    population = numpy.array([570, 590, 630, 640, 712, 733, 750])
    fitted = Cagr().fit(population).fitted()
    assert fitted[0] == pytest.approx(570)
    assert fitted[-1] == pytest.approx(750)


def test_linear_fits_a_straight_line_exactly():
    model = Linear().fit(numpy.array([10, 20, 30, 40]))
    assert model.fitted() == pytest.approx([10, 20, 30, 40])
    assert model.predict(2) == pytest.approx([50, 60])


def test_fibonacci_has_no_fitted_values():
    with pytest.raises(NotImplementedError):
        FobonacciRatio().fit(numpy.array([1, 2, 3])).fitted()
