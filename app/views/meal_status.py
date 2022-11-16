from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget

from app import meal as meal_repo

DAYS = [
    "esmaspäev",
    "teisipäev",
    "kolmapäev",
    "neljapäev",
    "reede",
    "laupäev",
    "pühapäev",
]

MEAL_TYPES = ["hommik", "lõuna", "vahepala", "õhtu"]


class MealStatusView(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self._show_weekday_names()
        self._show_meal_type_names()
        self._show_meal_buttons()

    def _show_weekday_names(self):
        for i, day in enumerate(DAYS, start=1):
            self.grid.addWidget(QLabel(day.capitalize(), self), i, 0)

    def _show_meal_type_names(self):
        for i, meal_type in enumerate(MEAL_TYPES, start=1):
            label = QLabel(meal_type.capitalize(), self)
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.grid.addWidget(label, 0, i)

    def _show_meal_buttons(self):
        weekday_and_type_to_meal = meal_repo.read_all_meals()
        for i in range(1, len(DAYS) + 1):
            weekday = DAYS[i - 1]
            for j in range(1, len(MEAL_TYPES) + 1):
                meal_type = MEAL_TYPES[j - 1]
                try:
                    meal = weekday_and_type_to_meal[(weekday, meal_type)]
                except KeyError:
                    button = QPushButton("❌")
                else:
                    button = QPushButton("✅") if meal.name else QPushButton("❌")
                self.grid.addWidget(button, i, j)
