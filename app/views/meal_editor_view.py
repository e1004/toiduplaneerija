import logging
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from app import meal as meal_repo
from app.meal import Meal

LOG = logging.getLogger(__file__)


class MealEditor(QDialog):
    def __init__(self, weekday: str, meal_type: str, meal: Meal, parent: QPushButton):
        super().__init__()
        self.parent_button = parent
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
        lower_buttons_row = QHBoxLayout()

        self.save_name_button = QPushButton("Salvesta nimi")
        self.save_name_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_name_button.clicked.connect(self.save_name)  # type: ignore
        lower_buttons_row.addWidget(self.save_name_button)

        self.layout.addLayout(lower_buttons_row)

    def save_name(self):
        new_name = self.name_field.text()
        meal = meal_repo.update_meal_name(
            name=new_name, weekday=self.weekday, meal_type=self.meal_type
        )
        LOG.info(f"save name pressed for {meal}")
        self.parent_button.setText("✅" if meal.name else "❌")
