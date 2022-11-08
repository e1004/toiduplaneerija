from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import meal
from meal import Meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_reads_all_meals():
    # given
    tuesday = "teisipäev"
    wednesday = "kolmapäev"
    friday = "reede"
    morning = "hommik"
    meal.add_empty_meal(weekday=tuesday, meal_type=morning)
    meal.update_meal_name(name="meal 1", weekday=tuesday, meal_type=morning)
    meal.add_empty_meal(weekday=wednesday, meal_type=morning)
    meal.update_meal_name(name="meal 2", weekday=wednesday, meal_type=morning)
    meal_3 = meal.add_empty_meal(weekday=friday, meal_type=morning)

    # when
    result = meal.read_all_meals()

    # then
    assert result == {
        ("kolmapäev", "hommik"): Meal(
            name="meal 2", ingredients=None, weekday="kolmapäev", meal_type="hommik"
        ),
        ("reede", "hommik"): Meal(
            name=None, ingredients=None, weekday="reede", meal_type="hommik"
        ),
        ("teisipäev", "hommik"): Meal(
            name="meal 1", ingredients=None, weekday="teisipäev", meal_type="hommik"
        ),
    }
