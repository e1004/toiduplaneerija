from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget

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

    def _show_weekday_names(self):
        for i, day in enumerate(DAYS, start=1):
            self.grid.addWidget(QLabel(day.capitalize(), self), i, 0)

    def _show_meal_type_names(self):
        for i, meal_type in enumerate(MEAL_TYPES, start=1):
            label = QLabel(meal_type.capitalize(), self)
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.grid.addWidget(label, 0, i)
