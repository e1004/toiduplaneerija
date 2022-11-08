import sqlite3
from contextlib import closing
from dataclasses import dataclass
from typing import Optional

from db import DB_NAME

INGREDIENT_SEPARATOR = "---separator---"


@dataclass
class Meal:
    name: Optional[str]
    ingredients: Optional[str]
    weekday: str
    meal_type: str

    @classmethod
    def make(
        cls, _cursor: sqlite3.Cursor, row: Optional[sqlite3.Row]
    ) -> Optional["Meal"]:
        if not row:
            return None
        return Meal(*row)


def add_empty_meal(weekday: str, meal_type: str) -> Meal:
    with closing(sqlite3.connect(DB_NAME, uri=True)) as connection:
        connection.row_factory = Meal.make
        with closing(connection.cursor()) as cursor:
            result: Meal = cursor.execute(
                ("INSERT INTO meal (weekday, meal_type) VALUES (?, ?)" "RETURNING *"),
                (weekday, meal_type),
            ).fetchone()
        connection.commit()
    return result


def update_meal_name(name: str, weekday: str, meal_type: str) -> Optional[Meal]:
    with closing(sqlite3.connect(DB_NAME, uri=True)) as connection:
        connection.row_factory = Meal.make
        with closing(connection.cursor()) as cursor:
            result: Optional[Meal] = cursor.execute(
                (
                    "UPDATE meal SET name = ? WHERE weekday = ? AND meal_type = ?"
                    "RETURNING *"
                ),
                (name, weekday, meal_type),
            ).fetchone()
        connection.commit()
    return result


def delete_meal(weekday: str, meal_type: str) -> Optional[Meal]:
    with closing(sqlite3.connect(DB_NAME, uri=True)) as connection:
        connection.row_factory = Meal.make
        with closing(connection.cursor()) as cursor:
            result: Optional[Meal] = cursor.execute(
                ("DELETE FROM meal WHERE weekday = ? AND meal_type = ? RETURNING *"),
                (weekday, meal_type),
            ).fetchone()
        connection.commit()
    return result


def read_all_meals() -> dict[tuple[str, str], Meal]:
    with closing(sqlite3.connect(DB_NAME, uri=True)) as connection:
        connection.row_factory = Meal.make
        with closing(connection.cursor()) as cursor:
            existing_meals: list[Meal] = cursor.execute(
                ("SELECT * FROM meal")
            ).fetchall()
    result: dict[tuple[str, str], Meal] = {}
    for meal in existing_meals:
        result[(meal.weekday, meal.meal_type)] = meal
    return result


def add_ingredient(ingredient: str, weekday: str, meal_type: str) -> Optional[Meal]:
    with closing(sqlite3.connect(DB_NAME, uri=True)) as connection:
        connection.row_factory = Meal.make
        with closing(connection.cursor()) as cursor:
            existing_meal: Optional[Meal] = cursor.execute(
                ("SELECT * FROM meal WHERE weekday = ? AND meal_type = ?"),
                (weekday, meal_type),
            ).fetchone()

            if not existing_meal:
                return None
            if existing_meal.ingredients is None:
                new_ingredients = ingredient
            else:
                if ingredient in existing_meal.ingredients:
                    return existing_meal
                new_ingredients = (
                    existing_meal.ingredients + INGREDIENT_SEPARATOR + ingredient
                )

            result: Optional[Meal] = cursor.execute(
                (
                    "UPDATE meal SET ingredients = ? WHERE weekday = ? AND meal_type = ?"
                    "RETURNING *"
                ),
                (new_ingredients, weekday, meal_type),
            ).fetchone()
        connection.commit()
    return result


def remove_ingredient(ingredient: str, weekday: str, meal_type: str) -> Optional[Meal]:
    with closing(sqlite3.connect(DB_NAME, uri=True)) as connection:
        connection.row_factory = Meal.make
        with closing(connection.cursor()) as cursor:
            existing_meal: Optional[Meal] = cursor.execute(
                ("SELECT * FROM meal WHERE weekday = ? AND meal_type = ?"),
                (weekday, meal_type),
            ).fetchone()

            if not existing_meal:
                return None
            if existing_meal.ingredients is None:
                return existing_meal
            if ingredient not in existing_meal.ingredients:
                return existing_meal

            existing_ingredients = existing_meal.ingredients.split(INGREDIENT_SEPARATOR)
            existing_ingredients.remove(ingredient)
            new_ingredients: Optional[str] = INGREDIENT_SEPARATOR.join(
                existing_ingredients
            )

            if new_ingredients == "":
                new_ingredients = None

            result: Optional[Meal] = cursor.execute(
                (
                    "UPDATE meal SET ingredients = ? WHERE weekday = ? AND meal_type = ?"
                    "RETURNING *"
                ),
                (new_ingredients, weekday, meal_type),
            ).fetchone()
        connection.commit()
    return result
