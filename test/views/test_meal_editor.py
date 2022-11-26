from app.meal import Meal
from app.views.meal_editor_view import MealEditor


def test_it_shows_weekdays_in_first_column(qtbot):
    # given
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name="any_name", ingredients=None, weekday=weekday, meal_type=meal_type)

    # when
    result = MealEditor(weekday, meal_type, meal)

    # then
    assert result.weekday == weekday
    assert result.meal_type == meal_type
    assert result.windowTitle() == "Any_weekday any_meal_type"


def test_it_has_empty_meal_name_for_missing_meal(qtbot):
    # given
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = None
    editor = MealEditor(weekday, meal_type, meal)

    # when
    result = editor.name_field.text()

    # then
    assert result == ""


def test_it_has_empty_meal_name_for_nameless_meal(qtbot):
    # given
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name=None, ingredients=None, weekday=weekday, meal_type=meal_type)
    editor = MealEditor(weekday, meal_type, meal)

    # when
    result = editor.name_field.text()

    # then
    assert result == ""
