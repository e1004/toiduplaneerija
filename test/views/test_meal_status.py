from test.db import TEST_DB_NAME

import pytest
from PyQt6.QtCore import Qt
from pytest_mock import MockerFixture

from app import meal
from app.views.meal_editor_view import MealEditor
from app.views.meal_status import DAYS, MEAL_TYPES, MealStatusView


@pytest.fixture
def use_test_db(db_connection, mocker: MockerFixture):
    mocker.patch.object(meal, "DB_NAME", TEST_DB_NAME)


@pytest.fixture
def view(qtbot):
    yield MealStatusView()


def test_it_shows_weekdays_in_first_column(view: MealStatusView):
    # when
    result = [
        view.grid.itemAtPosition(i, 0).widget().text().lower() for i in range(1, 8)
    ]

    # then
    assert result == DAYS


def test_it_has_only_7_days(view: MealStatusView):
    # when
    result = view.grid.itemAtPosition(8, 0)

    # then
    assert result is None


def test_it_shows_meal_types_in_first_row(view: MealStatusView):
    # when
    result = [
        view.grid.itemAtPosition(0, i).widget().text().lower() for i in range(1, 5)
    ]

    # then
    assert result == MEAL_TYPES


def test_it_has_only_4_meal_types(view: MealStatusView):
    # when
    result = view.grid.itemAtPosition(0, 5)

    # then
    assert result is None


@pytest.mark.usefixtures("use_test_db")
def test_it_has_buttons_for_nameless_meals(view: MealStatusView):
    # when
    result = [
        view.grid.itemAtPosition(i, j).widget().text()
        for i in range(1, 8)
        for j in range(1, 5)
    ]

    # then
    assert result == ["❌" for i in range(28)]


@pytest.mark.usefixtures("use_test_db")
def test_it_has_buttons_for_meals_with_names(qtbot):
    # given
    weekday = "teisipäev"
    meal_type = "hommik"
    meal.add_empty_meal(weekday, meal_type)
    meal.update_meal_name("any_name", weekday, meal_type)
    view = MealStatusView()

    # when
    result = [
        view.grid.itemAtPosition(i, j).widget().text()
        for i in range(1, 8)
        for j in range(1, 5)
    ]

    # then
    assert result == ["❌" for i in range(4)] + ["✅"] + ["❌" for i in range(23)]


def test_button_opens_meal_editor(view: MealStatusView, qtbot, mocker: MockerFixture):
    # given
    button = view.grid.itemAtPosition(1, 1).widget()
    editor_init = mocker.patch.object(MealEditor, "__init__", return_value=None)
    exec = mocker.patch.object(MealEditor, "exec")

    # when
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # then
    editor_init.assert_called_once_with("esmaspäev", "hommik")
    exec.assert_called_once()
