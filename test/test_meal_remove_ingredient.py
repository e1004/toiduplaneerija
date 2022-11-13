from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import app.meal as meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_removes_final_ingredient():
    # given
    new_ingredient = "any_ingredient"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"
    meal.add_empty_meal(any_weekday, any_meal_type)
    meal.add_ingredient(new_ingredient, any_weekday, any_meal_type)

    # when
    result = meal.remove_ingredient(new_ingredient, any_weekday, any_meal_type)

    # then
    assert result == meal.Meal(
        name=None,
        ingredients=None,
        weekday=any_weekday,
        meal_type=any_meal_type,
    )


def test_it_returns_meal_if_ingredient_missing():
    # given
    new_ingredient = "any_ingredient"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"
    meal.add_empty_meal(any_weekday, any_meal_type)

    # when
    result = meal.remove_ingredient(new_ingredient, any_weekday, any_meal_type)

    # then
    assert result == meal.Meal(
        name=None,
        ingredients=None,
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


def test_it_removes_ingredient_and_keeps_other_ingredients():
    # given
    ingredient_1, ingredient_2, ingredient_3, = (
        "any_i1",
        "any_i2",
        "any_i3",
    )
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"
    meal.add_empty_meal(any_weekday, any_meal_type)
    meal.add_ingredient(ingredient_1, any_weekday, any_meal_type)
    meal.add_ingredient(ingredient_2, any_weekday, any_meal_type)
    meal.add_ingredient(ingredient_1, any_weekday, any_meal_type)
    meal.add_ingredient(ingredient_3, any_weekday, any_meal_type)

    # when
    result = meal.remove_ingredient(
        ingredient_2, weekday=any_weekday, meal_type=any_meal_type
    )

    # then
    assert result == meal.Meal(
        name=None,
        ingredients=f"{ingredient_1}{meal.INGREDIENT_SEPARATOR}{ingredient_3}",
        weekday=any_weekday,
        meal_type=any_meal_type,
    )
