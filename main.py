import sys
from PyQt5.QtWidgets import QApplication
from app_database.cocktail_db import CocktailDB
from app_database.inventory_db import InventoryDB
from app_gui.main_window import MainWindow


def main():
    # Initialize the database handlers.
    inventory_db = InventoryDB()
    cocktail_db = CocktailDB()

    # Load data into in-memory caches.
    inventory_cache = inventory_db.load_cache()
    cocktail_cache = cocktail_db.load_cache()

    # (Optional) Pass these caches to your logic or GUI modules if needed.
    app = QApplication(sys.argv)
    window = MainWindow(inventory_cache, cocktail_cache, inventory_db, cocktail_db)  # Pass caches or handlers as needed
    window.show()
    app.exec_()

    # Close database connections on exit.
    inventory_db.close()
    cocktail_db.close()


if __name__ == "__main__":
    main()
