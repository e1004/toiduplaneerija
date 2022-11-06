from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_updates_name():
    # given
    new_name = "any_name"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"
    meal.add_empty_meal(any_weekday, any_meal_type)

    # when
    result = meal.update_meal_name(new_name, any_weekday, any_meal_type)

    # then
    assert result == meal.Meal(
        name=new_name, ingredients=None, weekday=any_weekday, meal_type=any_meal_type
    )


def test_it_returns_none_for_missing_meal():
    # given
    new_name = "any_name"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"

    # when
    result = meal.update_meal_name(new_name, any_weekday, any_meal_type)

    # then
    assert result is None
