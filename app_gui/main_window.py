# main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, inventory_cache, cocktail_cache, inventory_db, cocktail_db):
        """
        :param inventory_cache: dict loaded from InventoryDB (keys are canonical ingredient names).
        :param cocktail_cache: dict loaded from CocktailDB (each cocktail has an "ingredients" key,
                               which is a list of dicts containing ingredient details).
        :param inventory_db: InventoryDB handler (for refreshing/updating inventory).
        :param cocktail_db: CocktailDB handler.
        """
        super().__init__()
        self.inventory_cache = inventory_cache
        self.cocktail_cache = cocktail_cache
        self.inventory_db = inventory_db
        self.cocktail_db = cocktail_db

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cocktail App")
        # Create a central widget with a dark background.
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #222;")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- "Your Stats" Section ---
        stats_title = QLabel("Your Stats")
        stats_title.setStyleSheet("color: white; font: bold 16pt;")
        main_layout.addWidget(stats_title, alignment=Qt.AlignLeft)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        # Stat Box 1: Cocktails you can make (Purple)
        self.box_makeable = self.createStatBox("Cocktails you can make:", "71", "#800080")
        stats_layout.addWidget(self.box_makeable)

        # Stat Box 2: Cocktails made so far (Green)
        self.box_made = self.createStatBox("Cocktails made so far:", "23", "#008000")
        stats_layout.addWidget(self.box_made)

        # Stat Box 3: Total Bar Ingredients (Red)
        self.box_ingredients = self.createStatBox("Total Bar Ingredients:", "12", "#FF0000")
        stats_layout.addWidget(self.box_ingredients)

        main_layout.addLayout(stats_layout)

        # --- "Make a Cocktail" Section ---
        make_title = QLabel("Make a Cocktail")
        make_title.setStyleSheet("color: white; font: bold 16pt;")
        main_layout.addWidget(make_title, alignment=Qt.AlignLeft)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Surprise Me button (red-tinted)
        self.btn_surprise = QPushButton("Surprise Me")
        self.btn_surprise.setStyleSheet("background-color: #b22222; color: white; font: bold 12pt; padding: 10px;")
        self.btn_surprise.clicked.connect(self.surprise_me)
        button_layout.addWidget(self.btn_surprise)

        # Open Cocktails Book button (yellow-tinted)
        self.btn_book = QPushButton("Open Cocktails Book")
        self.btn_book.setStyleSheet("background-color: #d4af37; color: white; font: bold 12pt; padding: 10px;")
        self.btn_book.clicked.connect(self.open_cocktails_book)
        button_layout.addWidget(self.btn_book)

        # My Bar button (green-tinted)
        self.btn_my_bar = QPushButton("My Bar")
        self.btn_my_bar.setStyleSheet("background-color: #228b22; color: white; font: bold 12pt; padding: 10px;")
        self.btn_my_bar.clicked.connect(self.my_bar)
        button_layout.addWidget(self.btn_my_bar)

        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # (Optional) Update stats here by calling self.updateStats() when ready.
        self.updateStats()

    def createStatBox(self, label_text, value_text, bg_color):
        """
        Creates a rectangular stat box with a given background color.
        """
        box = QFrame()
        box.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px;")
        box.setFixedSize(150, 100)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(label_text)
        label.setStyleSheet("color: white; font: bold 12pt;")
        label.setWordWrap(True)
        value = QLabel(value_text)
        value.setStyleSheet("color: white; font: bold 20pt;")
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(value, alignment=Qt.AlignCenter)

        box.setLayout(layout)
        return box

    def updateStats(self):
        """
        Placeholder for updating stats values.
        Here you would update the stat boxes based on your logic, for example:
          - Count of cocktails that can be made (using can_make_cocktail on each recipe).
          - Count of cocktails made so far (perhaps stored in your cocktail_db).
          - Total ingredients in your inventory.
        For now, the values are hard-coded.
        """
        # Example (dummy) implementation:
        # num_makeable = sum(1 for cocktail in self.cocktail_cache.values()
        #                    if self.can_make_cocktail(cocktail.get("ingredients", [])))
        # self.box_makeable.findChild(QLabel).setText(str(num_makeable))
        pass

    def surprise_me(self):
        """
        Placeholder function for the "Surprise Me" button.
        You might choose a random cocktail from those that can be made.
        """
        print("Surprise Me clicked")
        # Example: Get list of possible cocktails, pick one at random and display details.
        possible = [cocktail["name"] for cocktail in self.cocktail_cache.values()
                    if self.can_make_cocktail(cocktail.get("ingredients", []))]
        if possible:
            print("You can make:", possible)
        else:
            print("No cocktails can be made with the current inventory.")

    def open_cocktails_book(self):
        """
        Placeholder function for opening the cocktails book.
        """
        print("Open Cocktails Book clicked")
        # Later, open the window showing all cocktail recipes.
        pass

    def my_bar(self):
        """
        Placeholder function for the "My Bar" button.
        This might show your full inventory.
        """
        print("My Bar clicked")
        # Later, open the inventory details window.
        pass

    # -----------
    # LOGIC FUNCTIONS
    # -----------

    def canonicalize(self, ingredient):
        """
        Converts an ingredient name into its canonical form based on synonyms.
        For example, "lime", "fresh lime", and "lime juice" are all mapped to "lime juice".
        """
        synonyms = {
            "lime": "lime juice",
            "fresh lime": "lime juice",
            "lime juice": "lime juice",
            "lemon": "lemon juice",
            "lemon juice": "lemon juice"
            # Add more synonyms as needed.
        }
        return synonyms.get(ingredient.lower(), ingredient.lower())

    def can_make_cocktail(self, cocktail_recipe):
        """
        Checks if a cocktail can be made with the current inventory.

        :param cocktail_recipe: List of dicts where each dict contains:
               "ingredient_name", "quantity_required", "unit".
        :return: True if every required ingredient is available in sufficient quantity.
        """
        for req in cocktail_recipe:
            canon_ing = self.canonicalize(req["ingredient_name"])
            inv_item = self.inventory_cache.get(canon_ing)
            if not inv_item or inv_item.get("quantity", 0) < req["quantity_required"]:
                return False
        return True

    def missing_ingredients(self, cocktail_recipe):
        """
        Returns a list of missing (or insufficient) ingredients for a cocktail recipe.
        Each ingredient name is canonicalized.

        :param cocktail_recipe: List of required ingredient dicts.
        :return: List of canonical ingredient names that are missing or under-stocked.
        """
        missing = []
        for req in cocktail_recipe:
            canon_ing = self.canonicalize(req["ingredient_name"])
            inv_item = self.inventory_cache.get(canon_ing)
            if not inv_item or inv_item.get("quantity", 0) < req["quantity_required"]:
                missing.append(canon_ing)
        return missing

    def almost_make_cocktails(self):
        """
        Returns a list of tuples for cocktails that are "almost" makeable.
        Each tuple is of the form: (cocktail_name, [list of missing ingredients]),
        where the cocktail is missing exactly one ingredient.
        """
        almost_possible = []
        for cocktail in self.cocktail_cache.values():
            recipe = cocktail.get("ingredients", [])
            missing = self.missing_ingredients(recipe)
            if len(missing) == 1:
                almost_possible.append((cocktail["name"], missing))
        return almost_possible
