import pytest

from app.views.meal_status import DAYS, MealStatusView


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
