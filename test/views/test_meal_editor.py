from app.views.meal_editor_view import MealEditor


def test_it_shows_weekdays_in_first_column(qtbot):
    # given
    weekday = "any_weekday"
    meal_type = "any_meal_type"

    # when
    result = MealEditor(weekday, meal_type)

    # then
    assert result.weekday == weekday
    assert result.meal_type == meal_type
    assert result.windowTitle() == "Any_weekday any_meal_type"
