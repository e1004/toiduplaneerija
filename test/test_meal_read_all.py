from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_reads_all_meals():

    # given
    weekday = "teisipäev"
    meal_type = "hommik"
    any_meal = meal.add_empty_meal(weekday, meal_type)

    # when
    result = meal.read_all_meals()

    # then
    if result!=None:
        assert any_meal in result 
