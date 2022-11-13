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


class MealStatusView(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self._show_weekday_names()

    def _show_weekday_names(self):
        for i, day in enumerate(DAYS, start=1):
            self.grid.addWidget(QLabel(day.capitalize(), self), i, 0)
