import sqlite3
from app_database.inventory_db import InventoryDB
from app_database.cocktail_db import CocktailDB
from PyQt5.QtWidgets import QApplication
from app_gui.main_window import MainWindow  # Your PyQt main window


# conn = sqlite3.connect('app_database')
# c = conn.cursor()
#
# c.execute('''
#     CREATE TABLE IF NOT EXISTS students (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         age INTEGER,
#         grade TEXT
#     )
# ''')
#
# # Insert a record
# c.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ('Alice', 22, 'A'))
# conn.commit()
# conn.close()
#

def main():
    # Initialize the database handlers.
    inventory_db = InventoryDB()
    cocktail_db = CocktailDB()

    # Load data into in-memory caches.
    inventory_cache = inventory_db.load_cache()
    cocktail_cache = cocktail_db.load_cache()

    # (Optional) Pass these caches to your logic or GUI modules if needed.

    # Start the PyQt application.
    app = QApplication([])
    window = MainWindow(inventory_cache, cocktail_cache)  # Pass caches or handlers as needed
    window.show()
    app.exec_()

    # Close database connections on exit.
    inventory_db.close()
    cocktail_db.close()


if __name__ == "__main__":
    main()
