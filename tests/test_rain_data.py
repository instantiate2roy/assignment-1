import numpy
import pytest

import src.rain_data
from src.rain_data import RainData

KAMPALA = {'lat': 0.3476, 'lon': 32.5825}


class FakeResponse:
    """Stands in for the NASA POWER response, so the tests never use the network."""

    def __init__(self, monthly):
        self.monthly = monthly

    def raise_for_status(self):
        pass

    def json(self):
        return {'properties': {'parameter': {'PRECTOTCORR_SUM': self.monthly}}}


@pytest.fixture
def fake_api(monkeypatch, tmp_path):
    """Point the CSV files at a temporary folder and record every request made."""
    monkeypatch.setattr(RainData, 'base_file_dir', str(tmp_path))
    requests_made = []

    def respond(monthly):
        def fake_get(url, params=None, timeout=None):
            requests_made.append(params)
            return FakeResponse(monthly)
        monkeypatch.setattr(src.rain_data.requests, 'get', fake_get)
        return requests_made

    return respond


def two_years():
    # 2024 and 2025: month m has m * 10 mm; key 13 is NASA's annual total
    monthly = {f'{year}{month:02d}': month * 10.0 for year in (2024, 2025) for month in range(1, 13)}
    monthly.update({'202413': 780.0, '202513': 780.0})
    return monthly


def test_api_data_is_saved_and_loaded_by_year(fake_api, tmp_path):
    fake_api(two_years())
    data = RainData('Kampala', KAMPALA).get()

    assert list(data) == [2024, 2025]
    assert data[2024].tolist() == [m * 10.0 for m in range(1, 13)]
    lines = (tmp_path / 'Kampala_rain_data.csv').read_text().splitlines()
    assert lines[0] == 'year,month,rainfall_mm'
    assert len(lines) == 1 + 24              # the two annual totals are not saved as months


def test_request_uses_the_location_coordinates(fake_api):
    requests_made = fake_api(two_years())
    RainData('Kampala', KAMPALA).get()
    assert requests_made[0]['latitude'] == 0.3476
    assert requests_made[0]['longitude'] == 32.5825
    assert requests_made[0]['parameters'] == 'PRECTOTCORR_SUM'


def test_missing_months_become_nan(fake_api):
    # Edge case: NASA marks missing values as -999
    monthly = two_years()
    monthly['202402'] = -999
    fake_api(monthly)
    data = RainData('Kampala', KAMPALA).get()
    assert numpy.isnan(data[2024][1])
    assert not numpy.isnan(numpy.delete(data[2024], 1)).any()


# Edge cases: the API is unreachable

@pytest.fixture
def offline(monkeypatch, tmp_path):
    monkeypatch.setattr(RainData, 'base_file_dir', str(tmp_path))

    def fail(*args, **kwargs):
        raise src.rain_data.requests.ConnectionError('no network')
    monkeypatch.setattr(src.rain_data.requests, 'get', fail)


def test_offline_falls_back_to_the_saved_file(offline, tmp_path):
    rows = ''.join(f'2024,{month:02d},{month * 10}\n' for month in range(1, 13))
    (tmp_path / 'Kampala_rain_data.csv').write_text('year,month,rainfall_mm\n' + rows)
    data = RainData('Kampala', KAMPALA).get()
    assert data[2024].tolist() == [m * 10.0 for m in range(1, 13)]


def test_offline_without_a_saved_file_is_reported(offline):
    with pytest.raises(FileNotFoundError):
        RainData('Kampala', KAMPALA).get()
