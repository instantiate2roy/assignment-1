import math

import numpy
import pytest

from src.district_population import DistrictPopulation
from src.validate import Validate

YEARS = numpy.arange(2015, 2025)
KAMPALA = numpy.array([1200, 1250, 1300, 1350, 1420, 1500, 1580, 1650, 1720, 1800])


@pytest.fixture
def kampala():
    return DistrictPopulation(Validate(), YEARS, KAMPALA, 'Kampala')


def test_statistics_std_matches_statistics_variance(kampala):
    # Both use N - 1 in statistics mode, so std squared must equal variance
    assert kampala.standard_deviation('statistics') ** 2 == pytest.approx(kampala.variance('statistics'))
    assert kampala.variance('statistics') > kampala.variance('numpy')


def test_first_year_growth_is_not_applicable(kampala):
    growth = kampala.year_on_year_growth()
    assert growth['2015'] == 'N/A'
    assert growth['2016'] == '4.167%'


def test_best_model_picks_lowest_errors(kampala):
    predictions = {
        'Actual-data': {'metrics': {'MAE': 'N/A', 'RMSE': 'N/A', 'MAPE': 'N/A'}},
        'Linear': {'metrics': {'MAE': 37.62, 'RMSE': 38.97, 'MAPE': 2.17}},
        'Cagr': {'metrics': {'MAE': 9.62, 'RMSE': 10.39, 'MAPE': 0.55}},
    }
    assert kampala.best_model(predictions) == 'Cagr'


def test_prediction_metrics(kampala):
    metrics = kampala.prediction_metrics(numpy.array([100, 200]), numpy.array([110, 190]))
    assert metrics == {'MAE': 10.0, 'RMSE': 10.0, 'MAPE': 7.5}


# Edge cases: invalid input must be rejected, not silently accepted

def test_years_and_population_length_mismatch_is_rejected():
    with pytest.raises(ValueError, match='same length'):
        DistrictPopulation(Validate(), YEARS, KAMPALA[:3], 'Kampala')


@pytest.mark.parametrize('population', [numpy.array([]), numpy.array([100, -5, 120])])
def test_empty_or_negative_population_is_rejected(population):
    with pytest.raises(ValueError):
        DistrictPopulation(Validate(), numpy.arange(len(population)), population, 'Bad')


def test_populations_of_different_lengths_are_rejected():
    with pytest.raises(ValueError, match='same number of entries'):
        Validate().populations([KAMPALA, KAMPALA[:7]])


def test_growth_from_zero_does_not_divide_by_zero():
    district = DistrictPopulation(Validate(), numpy.arange(3), numpy.array([0, 5, 10]), 'New')
    assert district.year_on_year_growth() == {'0': 'N/A', '1': 'N/A', '2': '100.0%'}
