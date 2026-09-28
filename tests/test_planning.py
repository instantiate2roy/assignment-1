import pytest

from src.planning import ClassroomPlanner


@pytest.fixture
def planner():
    return ClassroomPlanner(school_age_share=0.18, class_size=53, population_unit=1000)


def test_kampala_additional_classrooms(planner):
    # 1800 thousand in 2024 needs 6,114 classrooms; 2254.76 thousand in 2029 needs 7,658
    assert planner.classrooms_needed(1800) == 6114
    assert planner.classrooms_needed(2254.76) == 7658
    assert planner.additional_classrooms(1800, 2254.76) == 1544


def test_classrooms_round_up(planner):
    # 1 thousand people = 180 pupils = 3.4 classrooms, so 4 are needed
    assert planner.classrooms_needed(1) == 4


def test_shrinking_population_needs_no_new_classrooms(planner):
    assert planner.additional_classrooms(1800, 1500) == 0


def test_zero_population_needs_no_classrooms(planner):
    assert planner.classrooms_needed(0) == 0


@pytest.mark.parametrize('population', [-790, float('nan'), None, '790', True])
def test_invalid_population_is_rejected(planner, population):
    with pytest.raises(ValueError):
        planner.classrooms_needed(population)


@pytest.mark.parametrize('settings', [
    {'population_unit': 0},
    {'population_unit': -1000},
    {'class_size': 0},
    {'class_size': 52.5},
    {'school_age_share': 1.5},
    {'school_age_share': '0.18'},
])
def test_invalid_settings_are_rejected(settings):
    with pytest.raises(ValueError):
        ClassroomPlanner(**settings)
