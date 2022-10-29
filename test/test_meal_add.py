from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_adds_empty_meal():
    # given
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"

    # when
    result = meal.add_empty_meal(any_weekday, any_meal_type)

    # then
    assert result == meal.Meal(
        name=None, ingredients=None, weekday="esmaspäev", meal_type="õhtu"
    )
