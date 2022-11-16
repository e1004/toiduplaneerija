import logging
import sqlite3
import sys
from contextlib import closing

from PyQt6.QtWidgets import QApplication, QMainWindow

from app.db import CREATE_TABLE_MEAL, DB_NAME
from app.views.meal_status import MealStatusView

LOG = logging.getLogger(__file__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    LOG.info("application starting")

    with closing(sqlite3.connect(DB_NAME, uri=True)) as connection:
        connection.execute(CREATE_TABLE_MEAL)
    LOG.info("meal database table created")

    app = QApplication([])

    main_window = QMainWindow()
    main_window.setWindowTitle("Toiduplaan")

    meal_status_view = MealStatusView()
    meal_status_view.setParent(main_window)

    main_window.setCentralWidget(meal_status_view)
    main_window.show()

    sys.exit(app.exec())
