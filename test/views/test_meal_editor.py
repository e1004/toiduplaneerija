from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton
from pytest_mock import MockerFixture

from app import meal as meal_repo
from app.meal import Meal
from app.views.meal_editor_view import MealEditor


def test_it_sets_window_title(qtbot, mocker: MockerFixture):
    # given
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    parent = mocker.Mock()
    meal = Meal(name="any_name", ingredients=None, weekday=weekday, meal_type=meal_type)

    # when
    result = MealEditor(weekday, meal_type, meal, parent=parent)

    # then
    assert result.weekday == weekday
    assert result.meal_type == meal_type
    assert result.windowTitle() == "Any_weekday any_meal_type"


def test_it_has_empty_meal_name_for_nameless_meal(qtbot, mocker: MockerFixture):
    # given
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name=None, ingredients=None, weekday=weekday, meal_type=meal_type)
    parent = mocker.Mock()
    editor = MealEditor(weekday, meal_type, meal, parent=parent)

    # when
    result = editor.name_field.text()

    # then
    assert result == ""


def test_it_has_meal_name_for_meal_with_name(qtbot, mocker: MockerFixture):
    # given
    name = "any_name"
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name=name, ingredients=None, weekday=weekday, meal_type=meal_type)
    parent = mocker.Mock()
    editor = MealEditor(weekday, meal_type, meal, parent=parent)

    # when
    result = editor.name_field.text()

    # then
    assert result == name


def test_it_calls_meal_repo_update_name_with_empty_string_for_no_name(
    qtbot, mocker: MockerFixture
):
    # given
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name=None, ingredients=None, weekday=weekday, meal_type=meal_type)
    parent = mocker.Mock()
    editor = MealEditor(weekday, meal_type, meal, parent=parent)
    update_meal_name = mocker.patch.object(meal_repo, "update_meal_name")

    # when
    qtbot.mouseClick(editor.save_name_button, Qt.MouseButton.LeftButton)

    # then
    update_meal_name.assert_called_once_with(
        meal_type=meal_type, name="", weekday=weekday
    )


def test_it_calls_meal_repo_update_name_with_new_name(qtbot, mocker: MockerFixture):
    # given
    new_name = "any_new_name"
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name="any_name", ingredients=None, weekday=weekday, meal_type=meal_type)
    parent = mocker.Mock()
    editor = MealEditor(weekday, meal_type, meal, parent=parent)
    update_meal_name = mocker.patch.object(meal_repo, "update_meal_name")
    editor.name_field.setText(new_name)

    # when
    qtbot.mouseClick(editor.save_name_button, Qt.MouseButton.LeftButton)

    # then
    update_meal_name.assert_called_once_with(
        meal_type=meal_type, name=new_name, weekday=weekday
    )


def test_it_sets_parent_status_to_red_given_no_new_name(qtbot, mocker: MockerFixture):
    # given
    new_name = ""
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name="any_name", ingredients=None, weekday=weekday, meal_type=meal_type)
    new_meal = Meal(
        name=new_name, ingredients=None, weekday=weekday, meal_type=meal_type
    )
    parent = QPushButton()
    editor = MealEditor(weekday, meal_type, meal, parent=parent)
    mocker.patch.object(meal_repo, "update_meal_name", return_value=new_meal)
    editor.name_field.setText(new_name)

    # when
    qtbot.mouseClick(editor.save_name_button, Qt.MouseButton.LeftButton)

    # then
    assert parent.text() == "❌"


def test_it_sets_parent_status_to_green_given_new_name(qtbot, mocker: MockerFixture):
    # given
    new_name = "any_new_name"
    weekday = "any_weekday"
    meal_type = "any_meal_type"
    meal = Meal(name="any_name", ingredients=None, weekday=weekday, meal_type=meal_type)
    new_meal = Meal(
        name=new_name, ingredients=None, weekday=weekday, meal_type=meal_type
    )
    parent = QPushButton()
    editor = MealEditor(weekday, meal_type, meal, parent=parent)
    mocker.patch.object(meal_repo, "update_meal_name", return_value=new_meal)
    editor.name_field.setText(new_name)

    # when
    qtbot.mouseClick(editor.save_name_button, Qt.MouseButton.LeftButton)

    # then
    assert parent.text() == "✅"
