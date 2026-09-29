import csv
import math

import numpy
import pytest

from src.csv_generator import CsvGenerator
from src.microgrid import MicroGrid
from src.validate import Validate


@pytest.fixture
def grid():
    return MicroGrid()


def read_rows(path):
    with open(path, newline='') as file:
        return [{'day': int(r['day']), 'd1': float(r['d1']), 'd2': float(r['d2'])} for r in csv.DictReader(file)]


def test_determinant_and_condition_number(grid):
    # det = 3*1 - 2*4 = -5; the 2-norm condition number of [[3, 2], [4, 1]] is 3 + 2*sqrt(2)
    assert grid.determinant() == pytest.approx(-5)
    assert grid.condition() == pytest.approx(3 + 2 * math.sqrt(2))


def test_solve_matches_hand_calculation(grid):
    # By hand: x = (2*D2 - D1) / 5 = 8 and y = (4*D1 - 3*D2) / 5 = 38
    x, y = grid.solve_day(100, 70)
    assert (x, y) == pytest.approx((8, 38))
    assert 3 * x + 2 * y == pytest.approx(100)
    assert 4 * x + y == pytest.approx(70)


@pytest.mark.parametrize('d1, d2, negative', [(100, 150, 'battery'), (100, 40, 'solar')])
def test_some_demands_need_negative_supply(grid, d1, d2, negative):
    # D2 = 1.5 * D1 needs a negative battery draw, D2 = 0.4 * D1 a negative solar draw
    x, y = grid.solve_day(d1, d2)
    assert (y < 0) if negative == 'battery' else (x < 0)


def test_singular_coefficients_are_rejected(grid):
    # The second row is twice the first, so the determinant is 0 and there is no unique solution
    grid.co_efficients = [[1, 2], [2, 4]]
    with pytest.raises(ValueError):
        grid.determinant()


# Interactive input validation

@pytest.mark.parametrize('value', ['12.5', '0', '100'])
def test_valid_energy_input_is_accepted(value):
    Validate().check_energy_input(value)


@pytest.mark.parametrize('value', ['', None, '   ', 'abc', '12kWh', '-5'])
def test_invalid_energy_input_is_rejected(value):
    with pytest.raises(ValueError):
        Validate().check_energy_input(value)


# CSV generation

def test_csv_has_header_and_one_row_per_day(tmp_path):
    path = tmp_path / 'solar.csv'
    CsvGenerator().solar_grid_csv(path, n_days=30, seed_number=36)
    with open(path, newline='') as file:
        assert next(csv.reader(file)) == ['day', 'd1', 'd2']
    assert [row['day'] for row in read_rows(path)] == list(range(1, 31))


def test_same_seed_gives_the_same_data(tmp_path):
    first, second, other = tmp_path / 'a.csv', tmp_path / 'b.csv', tmp_path / 'c.csv'
    CsvGenerator().solar_grid_csv(first, seed_number=36)
    CsvGenerator().solar_grid_csv(second, seed_number=36)
    CsvGenerator().solar_grid_csv(other, seed_number=7)
    assert first.read_text() == second.read_text()
    assert first.read_text() != other.read_text()


def test_weekends_have_lower_demand(tmp_path):
    # Weekdays are 100 +/- 10 kWh for D1 and 70 +/- 7 for D2; days 6 and 7 of each week are 80 and 50
    path = tmp_path / 'solar.csv'
    CsvGenerator().solar_grid_csv(path, n_days=28, seed_number=36)
    for row in read_rows(path):
        weekend = (row['day'] - 1) % 7 in (5, 6)
        low, high = (70, 90) if weekend else (90, 110)
        assert low <= row['d1'] <= high
        low, high = (43, 57) if weekend else (63, 77)
        assert low <= row['d2'] <= high


def test_bad_data_breaks_the_expected_days(grid, tmp_path):
    path = tmp_path / 'solar_bad.csv'
    CsvGenerator().solar_grid_csv(path, n_days=30, seed_number=36, all_feasible=False)
    rows = {row['day']: row for row in read_rows(path)}

    # Days 5 and 25 have a negative D1 reading, day 15 a negative D2 reading
    assert rows[5]['d1'] < 0 and rows[25]['d1'] < 0
    assert rows[15]['d2'] < 0

    # Days 10 and 30 need a negative battery draw, day 20 a negative solar draw
    for day in (10, 30):
        assert grid.solve_day(rows[day]['d1'], rows[day]['d2'])[1] < 0
    assert grid.solve_day(rows[20]['d1'], rows[20]['d2'])[0] < 0

    # Every other day is left feasible
    for day, row in rows.items():
        if day % 5 != 0:
            assert numpy.all(grid.solve_day(row['d1'], row['d2']) >= 0)
