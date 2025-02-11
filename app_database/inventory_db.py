import sqlite3


class InventoryDB:
    def __init__(self, db_path='app_database/inventory.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()
        self.cache = {}  # This dictionary serves as our in-memory cache.

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                category TEXT
            )
        ''')
        self.connection.commit()

    def canonicalize(self, ingredient):
        """
        Converts an ingredient name to its canonical form.
        For example, "vodke" becomes "vodka", and "lemon" becomes "lemon juice".
        Adjust or add synonyms as needed.
        """
        synonyms = {
            "vodke": "vodka",
            "lemon": "lemon juice",
            "fresh lemon": "lemon juice"
            # Add more synonyms as needed.
        }
        return synonyms.get(ingredient.lower(), ingredient.lower())

    def load_cache(self):
        """
        Loads all ingredients from the database into the cache.
        The cache keys are the canonical names of the ingredients.
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT name, quantity, unit, category FROM ingredients')
        rows = cursor.fetchall()
        self.cache = {
            self.canonicalize(row[0]): {'quantity': row[1], 'unit': row[2], 'category': row[3]}
            for row in rows
        }
        return self.cache

    def add_ingredient(self, name, quantity, unit, category):
        """
        Inserts an ingredient into the database and updates the cache.
        The ingredient name is stored as its canonical version.
        """
        canonical_name = self.canonicalize(name)
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO ingredients (name, quantity, unit, category) 
            VALUES (?, ?, ?, ?)
        ''', (canonical_name, quantity, unit, category))
        self.connection.commit()
        self.cache[canonical_name] = {'quantity': quantity, 'unit': unit, 'category': category}

    def update_ingredient(self, name, quantity):
        """
        Updates the quantity of an ingredient (using its canonical name) in the database and cache.
        """
        canonical_name = self.canonicalize(name)
        cursor = self.connection.cursor()
        cursor.execute('UPDATE ingredients SET quantity=? WHERE name=?', (quantity, canonical_name))
        self.connection.commit()
        if canonical_name in self.cache:
            self.cache[canonical_name]['quantity'] = quantity

    def close(self):
        self.connection.close()


def load_sample_data(inventory_db):
    """
    Inserts a set of sample ingredients into the inventory database if they are not already present.
    The sample ingredients list:
      - gin, whisky, vodke, tripel sec, lemon, blue curacao, sloe gin, campari, simple syrup, passionfruit syrup.
    Each ingredient is inserted with a default quantity, unit, and category.
    """
    sample_ingredients = [
        {"name": "gin", "quantity": 1, "unit": "bottle", "category": "spirit"},
        {"name": "whisky", "quantity": 1, "unit": "bottle", "category": "spirit"},
        {"name": "vodke", "quantity": 1, "unit": "bottle", "category": "spirit"},
        {"name": "tripel sec", "quantity": 1, "unit": "bottle", "category": "liqueur"},
        {"name": "lemon", "quantity": 1, "unit": "item", "category": "fruit"},
        {"name": "blue curacao", "quantity": 1, "unit": "bottle", "category": "liqueur"},
        {"name": "sloe gin", "quantity": 1, "unit": "bottle", "category": "spirit"},
        {"name": "campari", "quantity": 1, "unit": "bottle", "category": "aperitif"},
        {"name": "simple syrup", "quantity": 1, "unit": "bottle", "category": "syrup"},
        {"name": "passionfruit syrup", "quantity": 1, "unit": "bottle", "category": "syrup"}
    ]

    # Load the current cache to check for existing ingredients.
    current_cache = inventory_db.load_cache()

    for ingredient in sample_ingredients:
        canonical_name = inventory_db.canonicalize(ingredient["name"])
        if canonical_name not in current_cache:
            inventory_db.add_ingredient(ingredient["name"], ingredient["quantity"],
                                        ingredient["unit"], ingredient["category"])
            print(f"Inserted ingredient: {canonical_name}")
        else:
            print(f"Ingredient already exists: {canonical_name}")

#
# if __name__ == '__main__':
#     inv_db = InventoryDB()
#     load_sample_data(inv_db)
#
#     # Print out the loaded inventory cache for verification.
#     cache = inv_db.load_cache()
#     print("Current Inventory Cache:")
#     for name, data in cache.items():
#         print(f"{name}: {data}")
#
#     inv_db.close()
