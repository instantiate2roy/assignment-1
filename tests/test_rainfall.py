import numpy
import pytest
from scipy.spatial.distance import cosine

from src.crop_rule import CropRule
from src.region import Region

KAMPALA = [120, 140, 180, 200, 220, 180, 90, 70, 60, 100, 110, 130]
GULU = [8, 25, 75, 160, 190, 145, 170, 215, 175, 150, 60, 15]
MBARARA = [70, 85, 120, 140, 90, 25, 20, 55, 100, 125, 120, 90]


@pytest.fixture
def kampala():
    return Region(numpy.array(KAMPALA), 'Kampala')


# Region statistics

def test_annual_total_and_mean(kampala):
    # 120 + 140 + ... + 130 = 1600 mm, so the monthly mean is 1600 / 12
    assert kampala.annual_total() == 1600
    assert kampala.mean() == pytest.approx(1600 / 12)


@pytest.mark.parametrize('rain, wettest, driest', [
    (KAMPALA, 'May', 'September'),
    (GULU, 'August', 'January'),
    (MBARARA, 'April', 'July'),
])
def test_wettest_and_driest_month(rain, wettest, driest):
    region = Region(numpy.array(rain), 'Region')
    assert region.wettest_month() == wettest
    assert region.driest_month() == driest


def test_coefficient_of_variation_is_std_over_mean(kampala):
    assert kampala.co_efficient_of_variation() == pytest.approx(numpy.std(KAMPALA) / numpy.mean(KAMPALA))


# Similarity and distance

def test_cosine_similarity_matches_scipy():
    assert Region.cosine_similarity(KAMPALA, GULU) == pytest.approx(1 - cosine(KAMPALA, GULU))


def test_cosine_similarity_ignores_how_much_rain_falls():
    # Twice the rain every month points the same way, so it scores a perfect 1
    assert Region.cosine_similarity(KAMPALA, numpy.array(KAMPALA) * 2) == pytest.approx(1)
    assert Region.cosine_similarity([1, 0], [0, 1]) == pytest.approx(0)


def test_pearson_correlation_matches_numpy():
    assert Region.pearson_correlation(KAMPALA, MBARARA) == pytest.approx(numpy.corrcoef(KAMPALA, MBARARA)[0, 1])
    assert Region.pearson_correlation(KAMPALA, numpy.array(KAMPALA) * -1) == pytest.approx(-1)


def test_euclidean_distance_picks_up_the_amount_of_rain():
    assert Region.euclidean_distance([0, 0], [3, 4]) == pytest.approx(5)
    # Doubling Kampala moves it exactly its own length away
    assert Region.euclidean_distance(KAMPALA, numpy.array(KAMPALA) * 2) == pytest.approx(numpy.linalg.norm(KAMPALA))


def test_sine_similarity_is_the_sine_of_the_angle():
    assert Region.sine_similarity([1, 0], [0, 1]) == pytest.approx(1)
    assert Region.sine_similarity(KAMPALA, KAMPALA) == pytest.approx(0, abs=1e-6)


# Edge cases: measures that are undefined must say so

@pytest.mark.parametrize('method', [Region.pearson_correlation, Region.euclidean_distance])
def test_vectors_of_different_lengths_are_rejected(method):
    with pytest.raises(ValueError):
        method([1, 2, 3], [1, 2])


def test_cosine_similarity_with_a_zero_vector_is_rejected():
    with pytest.raises(ValueError):
        Region.cosine_similarity([0, 0, 0], [1, 2, 3])


def test_pearson_correlation_with_no_variation_is_rejected():
    with pytest.raises(ValueError):
        Region.pearson_correlation([50] * 12, KAMPALA)


# Rainy seasons

@pytest.mark.parametrize('rain, peaks, pattern', [
    (MBARARA, ['April', 'October'], 'bimodal'),
    (GULU, ['August'], 'unimodal'),
])
def test_rainy_seasons(rain, peaks, pattern):
    seasons = Region(numpy.array(rain), 'Region').rainy_seasons()
    assert seasons['peak_months'] == peaks
    assert seasons['pattern'] == pattern


def test_a_rainy_season_across_new_year_counts_once():
    # Wettest in December and January: the year is treated as circular, so this is one season, not two
    rain = numpy.array([200, 150, 60, 40, 30, 30, 40, 60, 100, 150, 180, 220])
    seasons = Region(rain, 'Region').rainy_seasons()
    assert seasons['peak_months'] == ['December']
    assert seasons['pattern'] == 'unimodal'


# Crop rules

@pytest.mark.parametrize('rain, label', [
    (124.9, 'Drought risk'),
    (125, 'Good for maize'),
    (150, 'Good for maize'),
    (150.1, 'Waterlogging risk'),
])
def test_maize_range_includes_both_limits(kampala, rain, label):
    crop_rule = CropRule(kampala.rain_fall_data, 'Kampala')
    assert crop_rule.classification_by_crop(rain)['maize'] == label


def test_every_month_is_classified_for_every_crop():
    classes = CropRule(numpy.array(KAMPALA), 'Kampala').classify()
    assert list(classes) == Region.months
    assert all(set(crops) == {'maize', 'beans', 'coffee'} for crops in classes.values())
    # May has 220 mm: too wet for all three crops
    assert classes['May'] == {'maize': 'Waterlogging risk', 'beans': 'Waterlogging risk', 'coffee': 'Waterlogging risk'}


# Input validation

@pytest.mark.parametrize('rain', [
    [],                                   # no months
    KAMPALA[:11],                         # 11 months
    KAMPALA + [100],                      # 13 months
    [KAMPALA],                            # a 1 x 12 table instead of 12 values
    ['120'] * 12,                         # text
    [None] * 12,                          # missing values
    [True] * 12,                          # booleans
    KAMPALA[:11] + [float('nan')],        # NaN
    KAMPALA[:11] + [float('inf')],        # infinity
    KAMPALA[:11] + [-5],                  # negative rainfall
])
@pytest.mark.parametrize('model_class', [Region, CropRule])
def test_invalid_rainfall_is_rejected(model_class, rain):
    with pytest.raises(ValueError):
        model_class(rain, 'Region')


@pytest.mark.parametrize('name', ['', '   ', None, 42])
def test_invalid_region_name_is_rejected(name):
    with pytest.raises(ValueError):
        Region(numpy.array(KAMPALA), name)


def test_plain_lists_and_zero_months_are_accepted():
    region = Region([0] * 6 + [100] * 6, 'Dry half-year')
    assert region.annual_total() == 600


def test_coefficient_of_variation_with_no_rain_is_rejected():
    with pytest.raises(ValueError):
        Region([0] * 12, 'Desert').co_efficient_of_variation()


@pytest.mark.parametrize('rain', [-1, float('nan'), '120', None, True])
def test_invalid_monthly_rain_value_is_rejected(kampala, rain):
    with pytest.raises(ValueError):
        CropRule(kampala.rain_fall_data, 'Kampala').classification_by_crop(rain)
