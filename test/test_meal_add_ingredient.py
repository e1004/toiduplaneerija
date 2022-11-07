from test.db import TEST_DB_NAME

import pytest
from pytest_mock import MockerFixture

import meal


@pytest.fixture(autouse=True)
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


def test_it_adds_ingredient():
    # given
    new_ingredient = "any_ingredient"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"
    meal.add_empty_meal(any_weekday, any_meal_type)

    # when
    result = meal.add_ingredient(new_ingredient, any_weekday, any_meal_type)

    # then
    assert result == meal.Meal(
        name=None,
        ingredients=new_ingredient,
        weekday=any_weekday,
        meal_type=any_meal_type,
    )


def test_it_adds_ingredient_to_existing_ingredients():
    # given
    ingredient_1, ingredient_2, ingredient_3, = (
        "any_i1",
        "any_i2",
        "any_i3",
    )
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"
    meal.add_empty_meal(any_weekday, any_meal_type)

    # when
    result_1 = meal.add_ingredient(ingredient_1, any_weekday, any_meal_type)
    result_2 = meal.add_ingredient(ingredient_2, any_weekday, any_meal_type)
    result_3 = meal.add_ingredient(ingredient_1, any_weekday, any_meal_type)
    result_4 = meal.add_ingredient(ingredient_3, any_weekday, any_meal_type)

    # then
    assert result_1 == meal.Meal(
        name=None,
        ingredients=ingredient_1,
        weekday=any_weekday,
        meal_type=any_meal_type,
    )
    assert result_2.ingredients == (
        f"{ingredient_1}{meal.INGREDIENT_SEPARATOR}{ingredient_2}"
    )
    assert result_3 == result_2
    assert result_4.ingredients == (
        f"{ingredient_1}{meal.INGREDIENT_SEPARATOR}{ingredient_2}"
        f"{meal.INGREDIENT_SEPARATOR}{ingredient_3}"
    )


def test_it_returns_none_for_missing_meal():
    # given
    new_ingredient = "any_name"
    any_weekday = "esmaspäev"
    any_meal_type = "õhtu"

    # when
    result = meal.add_ingredient(new_ingredient, any_weekday, any_meal_type)

    # then
    assert result is None
