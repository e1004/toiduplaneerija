import logging
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
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
        self.ingredients: dict[QPushButton, QHBoxLayout] = {}
        self.setWindowTitle(weekday.capitalize() + " " + meal_type)
        self.layout: QVBoxLayout = QVBoxLayout()  # type: ignore
        self.setLayout(self.layout)

        self.name_field = QLineEdit()
        self.ingredient_field = QLineEdit()
        if meal and meal.name:
            self.name_field.setText(meal.name)
        self.name_field.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.name_field.setMinimumSize(400, 10)
        self.input_form = QFormLayout()
        self.input_form.addRow("Nimi: ", self.name_field)

        self.layout.addLayout(self.input_form)
        main_buttons_row = QHBoxLayout()
        ingredient_button_row = QHBoxLayout()
        self.ingredients_row = QFormLayout()

        self.save_name_button = QPushButton("Salvesta nimi 💾")
        self.save_name_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_name_button.clicked.connect(self.save_name)  # type: ignore

        self.delete_meal_button = QPushButton("Kustuta toidukord 🗑")
        self.delete_meal_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.delete_meal_button.clicked.connect(self.delete_meal)  # type: ignore

        self.save_ingredients_button = QPushButton("Salvesta koostisosad 🛒")
        self.save_ingredients_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_ingredients_button.clicked.connect(self.save_ingredients)  # type: ignore

        self.add_ingredient_button = QPushButton("+")
        self.add_ingredient_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.add_ingredient_button.setMaximumWidth(30)
        self.add_ingredient_button.clicked.connect(self.add_ingredient)  # type: ignore

        main_buttons_row.addWidget(self.save_name_button)
        main_buttons_row.addWidget(self.save_ingredients_button)
        main_buttons_row.addWidget(self.delete_meal_button)

        ingredient_button_row.addWidget(self.add_ingredient_button)

        self.layout.addLayout(main_buttons_row)
        self.layout.addWidget(QLabel("Koostisosad:"))
        self.layout.addLayout(self.ingredients_row)
        self.layout.addLayout(ingredient_button_row)

    def save_name(self):
        new_name = self.name_field.text()
        meal = meal_repo.update_meal_name(
            name=new_name, weekday=self.weekday, meal_type=self.meal_type
        )
        LOG.info(f"save name pressed for {meal}")
        self.parent_button.setText("✅" if meal.name else "❌")

    def delete_meal(self):
        deleted_meal = meal_repo.delete_meal(
            weekday=self.weekday, meal_type=self.meal_type
        )
        self.parent_button.setText("❌")
        LOG.info(f"deleted meal: {deleted_meal}")
        self.close()

    def save_ingredients(self):
        for ingredient_row in self.ingredients.values():
            ingredient = ingredient_row.itemAt(0).widget().text()
            meal_repo.add_ingredient(ingredient, self.weekday, self.meal_type)
            LOG.info(f"saving ingredient {ingredient}")

    # Ei tea kuidas saada, et koostisosa jäävad nähtavale

    def add_ingredient(self):
        ingredient_row = QHBoxLayout()
        ingredient_row.addWidget(QLineEdit())
        delete_ingredient_button = QPushButton("x")
        delete_ingredient_button.clicked.connect(self.delete_ingredient)
        ingredient_row.addWidget(delete_ingredient_button)
        self.ingredients[delete_ingredient_button] = ingredient_row
        self.ingredients_row.addRow(ingredient_row)
        LOG.info("ingredient added")

    def delete_ingredient(self):
        pushed_delete_ingredient_button = self.sender()
        ingredient_row = self.ingredients.pop(pushed_delete_ingredient_button)
        self.ingredients_row.removeRow(ingredient_row)
