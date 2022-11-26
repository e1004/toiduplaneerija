from PyQt6.QtWidgets import QDialog, QWidget


class MealEditor(QDialog):
    def __init__(self, weekday: str, meal_type: str):
        super().__init__()
        self.weekday = weekday
        self.meal_type = meal_type
        self.setWindowTitle(weekday.capitalize() + " " + meal_type)
