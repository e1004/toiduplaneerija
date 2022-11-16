DB_NAME = "meals.db"

CREATE_TABLE_MEAL = """
CREATE TABLE IF NOT EXISTS meal (
    name TEXT,
    ingredients TEXT,
    weekday TEXT NOT NULL check(
        "weekday" in (
            'esmaspäev',
            'teisipäev',
            'kolmapäev',
            'neljapäev',
            'reede',
            'laupäev',
            'pühapäev'
        )
    ),
    meal_type TEXT NOT NULL check(
        "meal_type" in (
            'hommik',
            'lõuna',
            'vahepala',
            'õhtu'
        )
    ),
    UNIQUE(weekday, meal_type) ON CONFLICT FAIL
);
"""
