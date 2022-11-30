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
        self.ingredient_field=QLineEdit()
        if meal and meal.name:
            self.name_field.setText(meal.name)
        self.name_field.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.name_field.setMinimumSize(400, 10)
        self.input_form = QFormLayout()
        self.input_form.addRow("Nimi: ", self.name_field)

        self.layout.addLayout(self.input_form)
        lower_buttons_row = QHBoxLayout()

        self.save_name_button = QPushButton("Salvesta nimi 💾")
        self.save_name_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_name_button.clicked.connect(self.save_name)  # type: ignore

        self.delete_name_button =QPushButton("Kustuta toidukord 🗑")
        self.delete_name_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.delete_name_button.clicked.connect(self.delete_name)

        self.save_ingredients_button =QPushButton("Salvesta koostisosad 🛒")
        self.save_ingredients_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_ingredients_button.clicked.connect(self.save_ingredients)

        self.add_row_button = QPushButton("+")
        self.add_row_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.add_row_button.clicked.connect(self.add_row)
        lower_buttons_row.addWidget(self.add_row_button)

        lower_buttons_row.addWidget(self.save_name_button)
        lower_buttons_row.addWidget(self.save_ingredients_button)
        lower_buttons_row.addWidget(self.delete_name_button)


        self.layout.addLayout(lower_buttons_row)

    def save_name(self):
        new_name = self.name_field.text()
        meal = meal_repo.update_meal_name(
            name=new_name, weekday=self.weekday, meal_type=self.meal_type
        )
        LOG.info(f"save name pressed for {meal}")
        self.parent_button.setText("✅" if meal.name else "❌")

    def delete_name(self):
        meal_repo.delete_meal(
            weekday=self.weekday, meal_type=self.meal_type
        ) 
        self.name_field.insert("")
        self.parent_button.setText("❌")
        meal_repo.add_empty_meal(weekday=self.weekday, meal_type=self.meal_type)
        LOG.info(f"deleted meal: {meal_repo}")
        MealEditor.close(self)

    def save_ingredients(self):
        global row_amount
        try:
            for i in range(row_amount):
                new_ingredient=self.ingredient_field.text()
                meal = meal_repo.add_ingredient(
                    ingredient=new_ingredient, weekday=self.weekday, meal_type=self.meal_type
                )
                print(meal)
                LOG.info(f"added ingredient: {new_ingredient}")
                row_amount=0
        except:
            row_amount=0
    #Ei tea kuidas saada, et koostisosa jäävad nähtavale


    def add_row(self):
        global row_amount
        try:
            row_amount+=1
        except:
            row_amount=1
        self.ingredients= QFormLayout()
        self.ingredients.addRow("Koostisosa "+str(row_amount)+":", QLineEdit())
        self.layout.addLayout(self.ingredients)
        LOG.info(f"added row")

