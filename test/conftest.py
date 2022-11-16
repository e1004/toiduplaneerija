import sqlite3
from contextlib import closing
from test.db import TEST_DB_NAME

import pytest

from app.db import CREATE_TABLE_MEAL


@pytest.fixture
def db_connection():
    with closing(sqlite3.connect(TEST_DB_NAME, uri=True)) as connection:
        connection.execute(CREATE_TABLE_MEAL)
        yield connection
        connection.execute("DELETE FROM meal")
