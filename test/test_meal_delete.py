import meal
from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_deletes_meal():
    # given
    weekday="teisipäev"
    meal_type="hommik"
    any_meal = meal.add_empty_meal(weekday, meal_type)

    # when
    result = meal.delete_meal(weekday, meal_type)

    # then
    assert result == any_meal

def test_it_returns_none_for_missing_meal():
    # given
    weekday="teisipäev"
    meal_type="hommik"

    # when
    result = meal.delete_meal(weekday, meal_type)

    # then
    assert result is None
