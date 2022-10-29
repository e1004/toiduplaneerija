import sqlite3
from calendar import weekday
from contextlib import closing
from dataclasses import dataclass
from typing import Optional

from db import DB_NAME


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
    with closing(sqlite3.connect(DB_NAME)) as connection:
        connection.row_factory = Meal.make
        with closing(connection.cursor()) as cursor:
            result = cursor.execute(
                ("INSERT INTO meal (weekday, meal_type) VALUES (?, ?)" "RETURNING *"),
                (weekday, meal_type),
            ).fetchone()
        connection.commit()
    return result
