import pytest

from src.closed_season_fish_stock import ClosedSeasonFishStock
from src.fish_stock import FishStock
from src.price_model import PriceModel
from src.risk_assesor import RiskAssessor


def fish_stock(model_class=FishStock, h=0.2):
    fish = model_class()
    fish.harvest_portion = h
    return fish


# Logistic growth with harvesting: N(t+1) = N(t) + r*N(t)*(1 - N(t)/K) - h*N(t)

def test_first_week_matches_hand_calculation():
    # growth = 0.4 * 4000 * (1 - 4000/10000) = 960, catch = 0.2 * 4000 = 800
    week_1 = fish_stock().simulate(1)[1]
    assert week_1 == pytest.approx({'stock': 4000, 'growth': 960, 'catch': 800, 'current_stock': 4160})


@pytest.mark.parametrize('h, resting_stock', [(0.1, 7500), (0.2, 5000), (0.3, 2500)])
def test_stock_settles_at_k_times_one_minus_h_over_r(h, resting_stock):
    final = fish_stock(h=h).simulate(52)[52]['current_stock']
    assert final == pytest.approx(resting_stock, rel=0.01)


def test_harvest_of_20_percent_gives_the_maximum_sustainable_yield():
    # MSY = r * K / 4 = 1000 t per week, reached when the stock sits at K / 2
    assert fish_stock(h=0.2).simulate(52)[52]['catch'] == pytest.approx(0.4 * 10000 / 4, rel=0.001)


def test_unharvested_stock_grows_towards_but_never_past_capacity():
    weeks = fish_stock(h=0).simulate(200)
    assert all(row['current_stock'] <= 10000 for row in weeks.values())
    assert weeks[200]['current_stock'] == pytest.approx(10000, rel=0.001)


def test_catch_can_never_exceed_the_fish_available():
    # Edge case: harvesting the whole stock each week never takes more fish than exist
    for week in fish_stock(h=1).simulate(10).values():
        assert week['catch'] <= week['stock'] + week['growth'] + 1e-9
        assert week['current_stock'] >= 0


@pytest.mark.parametrize('h', [-0.5, 1.5, '0.2', None, True, float('nan')])
def test_invalid_harvest_portion_is_rejected(h):
    with pytest.raises(ValueError):
        fish_stock(h=h)
    with pytest.raises(ValueError):
        FishStock(harvest_portion=h)


def test_closed_season_stock_validates_the_harvest_portion_too():
    with pytest.raises(ValueError):
        fish_stock(ClosedSeasonFishStock, h=-0.1)


def test_fibonacci_baseline():
    assert FishStock().generate_fibonacci_list(15)[-5:] == [89, 144, 233, 377, 610]
    assert FishStock().generate_fibonacci_list(0) == []


# Closed season

@pytest.mark.parametrize('week, closed', [(1, True), (8, True), (9, False), (52, False), (53, True), (61, False)])
def test_closed_season_is_weeks_1_to_8_of_every_year(week, closed):
    assert ClosedSeasonFishStock().is_closed(week) == closed


def test_no_catch_during_the_closed_season():
    weeks = fish_stock(ClosedSeasonFishStock).simulate(104)
    for week, row in weeks.items():
        if ClosedSeasonFishStock().is_closed(week):
            assert row['catch'] == 0
        else:
            assert row['catch'] > 0


def test_closed_season_changes_nothing_when_there_is_no_fishing():
    open_all_year = fish_stock(h=0).simulate(104)
    closed_season = fish_stock(ClosedSeasonFishStock, h=0).simulate(104)
    for week in open_all_year:
        assert closed_season[week] == pytest.approx(open_all_year[week])


# Price model

def test_price_starts_at_12000_and_stays_within_bounds():
    prices = PriceModel().simulate(2000)
    assert prices[1] == 12000
    assert all(9000 <= price <= 16000 for price in prices.values())
    assert all(price % 10 == 0 for price in prices.values())


def test_same_seed_gives_the_same_prices():
    other = PriceModel()
    other.seed = 7
    assert PriceModel().simulate(52) == PriceModel().simulate(52)
    assert PriceModel().simulate(52) != other.simulate(52)


# Risk assessment

@pytest.mark.parametrize('cv, risk', [(0.05, 'LOW'), (0.10, 'LOW'), (0.15, 'MODERATE'), (0.20, 'MODERATE'), (0.25, 'HIGH')])
def test_risk_class_by_coefficient_of_variation(cv, risk):
    assert RiskAssessor(FishStock(), PriceModel()).classify(cv) == risk


def test_run_gives_one_row_per_price_path_and_leaves_the_caller_seed_alone():
    prices = PriceModel()
    results = RiskAssessor(fish_stock(), prices, n_paths=200).run()
    assert len(results) == 200
    assert list(results.columns) == ['total_revenue', 'annual_revenue', 'weekly_cv']
    # 52 weeks is one year, so total and annual revenue are the same
    assert (results['total_revenue'] == results['annual_revenue']).all()
    assert prices.seed == 50


def test_value_at_risk_is_undercut_in_5_percent_of_years():
    assessor = RiskAssessor(fish_stock(), PriceModel(), n_paths=200)
    revenue = assessor.run()['annual_revenue']
    assert (revenue < assessor.value_at_risk(revenue)).sum() == 10


def test_annual_revenue_is_the_yearly_average_over_several_years():
    results = RiskAssessor(fish_stock(), PriceModel(), n_paths=20, weeks=5 * 52).run()
    assert results['annual_revenue'].to_numpy() == pytest.approx(results['total_revenue'].to_numpy() / 5)


def test_no_catch_gives_no_revenue_and_no_risk_class():
    # Edge case: with nothing caught the CV would divide by zero, so it is NaN and the class is N/A
    assessor = RiskAssessor(fish_stock(h=0), PriceModel(), n_paths=5)
    results = assessor.run()
    assert (results['total_revenue'] == 0).all()
    assert results['weekly_cv'].isna().all()
    assert assessor.classify(results['weekly_cv'].iloc[0]) == 'N/A'
