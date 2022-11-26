from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout

from app.meal import Meal


class MealEditor(QDialog):
    def __init__(self, weekday: str, meal_type: str, meal: Optional[Meal]):
        super().__init__()
        self.weekday = weekday
        self.meal_type = meal_type
        self.setWindowTitle(weekday.capitalize() + " " + meal_type)
        self.layout: QVBoxLayout = QVBoxLayout()  # type: ignore
        self.setLayout(self.layout)

        self.name_field = QLineEdit()
        if meal and meal.name:
            self.name_field.setText(meal.name)
        self.name_field.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.name_field.setMinimumSize(400, 10)
        self.input_form = QFormLayout()
        self.input_form.addRow("Nimi: ", self.name_field)

        self.layout.addLayout(self.input_form)
