from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem
)


class MainWindow(QMainWindow):
    def __init__(self, db_handler, data_cache):
        super().__init__()
        self.db_handler = db_handler
        self.data_cache = data_cache
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cocktail App")
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Inventory Label
        self.inv_label = QLabel("Inventory:")
        layout.addWidget(self.inv_label)

        # Inventory Table
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.refresh_inventory_table()

        # Refresh Button
        refresh_btn = QPushButton("Refresh Inventory")
        refresh_btn.clicked.connect(self.on_refresh)
        layout.addWidget(refresh_btn)

        # Cocktail Suggestion Status Label
        self.suggestion_label = QLabel("Cocktail Suggestion: Not checked")
        layout.addWidget(self.suggestion_label)

        # Test Cocktail Suggestion Button
        test_btn = QPushButton("Test Cocktail Suggestion")
        test_btn.clicked.connect(self.test_cocktail)
        layout.addWidget(test_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def refresh_inventory_table(self):
        """Refresh the table view with current inventory from the cache."""
        # Flatten the inventory dictionary to a list of ingredient records.
        inv_data = []
        for ing_list in self.data_cache.inventory.values():
            inv_data.extend(ing_list)
        self.table.setRowCount(len(inv_data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Unit"])
        for row, item in enumerate(inv_data):
            self.table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(item['name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            self.table.setItem(row, 3, QTableWidgetItem(item['unit']))

    def on_refresh(self):
        """Reload the inventory from the database and refresh the table."""
        self.data_cache.load_inventory()
        self.refresh_inventory_table()

    def test_cocktail(self):
        """
        Test the cocktail suggestion engine with a dummy cocktail recipe.
        For example, a cocktail that requires 60 ml of gin and 30 ml of lemon juice.
        """
        cocktail_recipe = [
            {"ingredient_name": "London Dry Gin", "quantity_required": 60, "unit": "ml"},
            {"ingredient_name": "lemon juice", "quantity_required": 30, "unit": "ml"}
        ]
        if self.data_cache.can_make_cocktail(cocktail_recipe):
            self.suggestion_label.setText("Cocktail can be made!")
        else:
            self.suggestion_label.setText("Not enough ingredients for cocktail.")
