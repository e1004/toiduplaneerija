from sqlite3 import IntegrityError
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


@pytest.mark.usefixtures("use_test_db")
def test_button_opens_meal_editor(view: MealStatusView, qtbot, mocker: MockerFixture):
    # given
    button = view.grid.itemAtPosition(1, 1).widget()
    editor_init = mocker.patch.object(MealEditor, "__init__", return_value=None)
    exec = mocker.patch.object(MealEditor, "exec")

    # when
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # then
    editor_init.assert_called_once_with(
        "esmaspäev",
        "hommik",
        meal.Meal(name=None, ingredients=None, weekday="esmaspäev", meal_type="hommik"),
        parent=button,
    )
    exec.assert_called_once()


@pytest.mark.usefixtures("use_test_db")
def test_button_creates_missing_empty_meal(
    view: MealStatusView, qtbot, mocker: MockerFixture
):
    # given
    button = view.grid.itemAtPosition(1, 1).widget()
    mocker.patch.object(MealEditor, "__init__", return_value=None)
    mocker.patch.object(MealEditor, "exec")
    weekday = "esmaspäev"
    meal_type = "hommik"

    # when
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # then
    try:
        meal.add_empty_meal(weekday, meal_type)
    except IntegrityError:
        pass
    else:
        pytest.fail("expected empty meal in db")


@pytest.mark.usefixtures("use_test_db")
def test_button_does_not_create_empty_meal_for_existing_nameless_meal(
    qtbot, mocker: MockerFixture
):
    # given
    weekday = "esmaspäev"
    meal_type = "hommik"
    existing_meal = meal.add_empty_meal(weekday, meal_type)
    view = MealStatusView()
    button = view.grid.itemAtPosition(1, 1).widget()
    editor_init = mocker.patch.object(MealEditor, "__init__", return_value=None)
    mocker.patch.object(MealEditor, "exec")
    add_empty_meal = mocker.spy(meal, "add_empty_meal")

    # when
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # then
    add_empty_meal.assert_not_called()
    editor_init.assert_called_once_with(
        "esmaspäev", "hommik", existing_meal, parent=button
    )


@pytest.mark.usefixtures("use_test_db")
def test_existing_meal_with_name_is_forwarded_to_meal_editor(
    qtbot, mocker: MockerFixture
):
    # given
    weekday = "esmaspäev"
    meal_type = "hommik"
    meal.add_empty_meal(weekday, meal_type)
    existing_meal = meal.update_meal_name("any_name", weekday, meal_type)
    view = MealStatusView()
    button = view.grid.itemAtPosition(1, 1).widget()
    editor_init = mocker.patch.object(MealEditor, "__init__", return_value=None)
    mocker.patch.object(MealEditor, "exec")
    add_empty_meal = mocker.spy(meal, "add_empty_meal")

    # when
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # then
    add_empty_meal.assert_not_called()
    editor_init.assert_called_once_with(
        "esmaspäev", "hommik", existing_meal, parent=button
    )


@pytest.mark.usefixtures("use_test_db")
def test_it_reads_all_meals_after_closing_meal_editor(qtbot, mocker: MockerFixture):
    # given
    weekday = "esmaspäev"
    meal_type = "hommik"
    meal.add_empty_meal(weekday, meal_type)
    view = MealStatusView()
    button = view.grid.itemAtPosition(1, 1).widget()
    mocker.patch.object(MealEditor, "exec")
    read_all_meals = mocker.spy(meal, "read_all_meals")

    # when
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # then
    assert view.weekday_and_type_to_meal == read_all_meals.spy_return
