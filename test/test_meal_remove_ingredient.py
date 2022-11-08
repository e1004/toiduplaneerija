from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_removes_ingredient():
    # given
    new_ingredient = "any_ingredient"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"
    meal.add_empty_meal(any_weekday, any_meal_type)
    meal.add_ingredient(new_ingredient, any_weekday, any_meal_type)
    # when 

    result = meal.remove_ingredient(new_ingredient,any_weekday,any_meal_type)
    # then
    assert result == meal.Meal(
        name=None,
        ingredients="",
        weekday=any_weekday,
        meal_type=any_meal_type,
    )

def test_it_returns_none_for_missing_meal():
    # given
    removable_ingredient = "any_name"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"

    # when
    result = meal.remove_ingredient(removable_ingredient, any_weekday, any_meal_type)

    # then
    assert result is None
