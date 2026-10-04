import statistics

import numpy
import pytest

from src.exponential_smoothing import ExponentialSmoothing
from src.matrix_equation import MatrixEquation
from src.moving_average import MovingAverage
from src.route import Route
from src.seasonal_naive import SeasonalNaive

NTINDA = [35, 40, 42, 50, 55, 60, 48, 52, 47, 45]


@pytest.fixture
def ntinda():
    return Route('Kampala-Ntinda', NTINDA, 2000)


# Route revenue

def test_daily_and_total_revenue(ntinda):
    # 474 passengers over 10 days at UGX 2,000 each
    assert ntinda.daily_revenue().tolist() == [n * 2000 for n in NTINDA]
    assert ntinda.total_revenue() == 948_000


def test_revenue_statistics_match_the_statistics_module(ntinda):
    revenue = [n * 2000 for n in NTINDA]
    assert ntinda.mean() == pytest.approx(94_800)
    assert ntinda.variance() == pytest.approx(statistics.variance(revenue))
    assert ntinda.std() == pytest.approx(statistics.stdev(revenue))


# Supply and demand equilibrium

def test_ntinda_equilibrium_matches_hand_calculation():
    # Q + 0.02P = 120 and Q - 0.03P = 10; subtracting gives 0.05P = 110, so P = 2,200 and Q = 76
    equation = MatrixEquation(numpy.array([[1, 0.02], [1, -0.03]]))
    quantity, price = equation.solve(120, 10)
    assert price == pytest.approx(2200)
    assert quantity == pytest.approx(76)
    assert equation.determinant() == pytest.approx(-0.05)


def test_equations_without_a_unique_solution_are_rejected():
    with pytest.raises(ValueError):
        MatrixEquation([[1, 2], [2, 4]]).determinant()


# Forecasters

def test_moving_average_predicts_the_mean_of_the_last_window():
    model = MovingAverage(3).fit([10, 20, 30, 40])
    # Day 5 is the mean of 20, 30, 40; day 6 rolls forward with that forecast: mean of 30, 40, 30
    assert model.predict(2) == pytest.approx([30, 100 / 3])
    fitted = model.fitted()
    assert numpy.isnan(fitted[:3]).all() and fitted[3] == pytest.approx(20)


def test_exponential_smoothing_matches_hand_calculation():
    # level = 0.5 * 20 + 0.5 * 10 = 15, and every future day is forecast at that level
    model = ExponentialSmoothing(0.5).fit([10, 20])
    assert model.predict(3) == pytest.approx([15, 15, 15])
    assert model.fitted()[1] == pytest.approx(10)


def test_exponential_smoothing_with_alpha_1_repeats_the_last_value():
    assert ExponentialSmoothing(1).fit(NTINDA).predict(1) == pytest.approx([NTINDA[-1]])


def test_seasonal_naive_repeats_the_last_week():
    two_weeks = list(range(1, 15))
    model = SeasonalNaive(7).fit(two_weeks)
    # The last week is days 8 to 14, and day 15 starts the next cycle with day 8's value
    assert model.predict(9).tolist() == [8, 9, 10, 11, 12, 13, 14, 8, 9]
    fitted = model.fitted()
    assert numpy.isnan(fitted[:7]).all()
    assert fitted[7:].tolist() == list(range(1, 8))


# Edge cases

@pytest.mark.parametrize('make_model', [
    lambda: MovingAverage(0),
    lambda: ExponentialSmoothing(0),
    lambda: ExponentialSmoothing(1.5),
    lambda: SeasonalNaive(0),
])
def test_invalid_settings_are_rejected(make_model):
    with pytest.raises(ValueError):
        make_model()


@pytest.mark.parametrize('model, data', [
    (MovingAverage(3), [10, 20]),
    (ExponentialSmoothing(0.5), []),
    (SeasonalNaive(7), [1, 2, 3]),
])
def test_too_little_data_is_rejected(model, data):
    with pytest.raises(ValueError):
        model.fit(data)


@pytest.mark.parametrize('model', [MovingAverage(3), ExponentialSmoothing(0.5), SeasonalNaive(7)])
def test_predict_before_fit_is_rejected(model):
    with pytest.raises(RuntimeError):
        model.predict(1)
