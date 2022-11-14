import pytest

from app.views.meal_status import DAYS, MEAL_TYPES, MealStatusView


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
