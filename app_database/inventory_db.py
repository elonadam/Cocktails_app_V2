import sqlite3
import json


class InventoryDB:
    def __init__(self, db_path='app_database/inventory.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()
        self.cache = {}  # In-memory cache of ingredients.

    def create_table(self):
        """Creates the inventory table with the new schema."""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bottle_name TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT,
                unit TEXT NOT NULL,
                quantity REAL NOT NULL,
                abv REAL,
                is_open INTEGER DEFAULT 1,
                curr_amount REAL
            )
        ''')
        self.connection.commit()

    def canonicalize(self, ingredient):
        """
        Converts an ingredient name to its canonical form.
        For example "lemon" becomes "lemon juice".
        Adjust or add synonyms as needed.
        """
        synonyms = {
            "lime": "lime juice",
            "fresh lime": "lime juice",
            "lemon": "lemon juice",
            "fresh lemon": "lemon juice",
            "ç": "c",
            # Add more synonyms as needed.
        }
        return synonyms.get(ingredient.lower(), ingredient.lower())

    def load_cache(self):
        """
        Loads all ingredients from the database into the in-memory cache.
        The cache keys are the canonical names of the bottle_name.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT bottle_name, quantity, unit, category, abv, is_open, curr_amount 
            FROM inventory
        ''')
        rows = cursor.fetchall()
        self.cache = {
            self.canonicalize(row[0]): {
                'quantity': row[1],
                'unit': row[2],
                'category': row[3],
                'abv': row[4],
                'is_open': row[5],
                'curr_amount': row[6]
            }
            for row in rows
        }
        return self.cache

    def add_ingredient(self, bottle_name, type, category, abv, unit, quantity, is_open, curr_amount):
        """
        Inserts an ingredient into the database and updates the cache.
        The bottle_name is stored in its canonical form.
        """
        canonical_name = self.canonicalize(bottle_name)
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO inventory (bottle_name, type, category, abv, unit, quantity, is_open, curr_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (canonical_name, type, category, abv, unit, quantity, is_open, curr_amount))
        self.connection.commit()
        self.cache[canonical_name] = {
            'quantity': quantity,
            'unit': unit,
            'category': category,
            'abv': abv,
            'is_open': is_open,
            'curr_amount': curr_amount
        }
        print(f"Inserted: {canonical_name}")

    def update_ingredient(self, bottle_name, quantity, curr_amount):
        """
        Updates the quantity and current amount of an ingredient (using its canonical bottle_name)
        in both the database and the in-memory cache.
        """
        canonical_name = self.canonicalize(bottle_name)
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE inventory
            SET quantity = ?, curr_amount = ?
            WHERE bottle_name = ?
        ''', (quantity, curr_amount, canonical_name))
        self.connection.commit()
        if canonical_name in self.cache:
            self.cache[canonical_name]['quantity'] = quantity
            self.cache[canonical_name]['curr_amount'] = curr_amount
            print(f"Updated: {canonical_name}")

    def import_from_json(self, json_file):
        """
        Imports ingredients from a JSON file into the inventory database.
        Each JSON object should include keys: bottle_name, type, category, abv, unit, quantity, is_open.
        If curr_amount is not provided, it defaults to the quantity.
        """
        with open(json_file, 'r', encoding='utf-8') as file:
            ingredients = json.load(file)
        for item in ingredients:
            self.add_ingredient(
                bottle_name=item["bottle_name"],
                type=item["type"],
                category=item["category"],
                abv=item["abv"],
                unit=item["unit"],
                quantity=item["quantity"],
                is_open=item["is_open"],
                curr_amount=item.get("curr_amount", item["quantity"])
            )

    def close(self):
        self.connection.close()


# def load_sample_data(inventory_db):
#     """
#     Inserts a set of sample ingredients into the inventory database if they are not already present.
#     This function is for testing purposes.
#     """
#     sample_ingredients = [
#         {"bottle_name": "Test Gin", "type": "Gin", "category": "spirit", "unit": "bottle", "quantity": 1, "abv": 40,
#          "is_open": 1, "curr_amount": 1},
#         {"bottle_name": "Test Whiskey", "type": "Whiskey", "category": "spirit", "unit": "bottle", "quantity": 1,
#          "abv": 40, "is_open": 1, "curr_amount": 1}
#     ]
#
#     current_cache = inventory_db.load_cache()
#     for ingredient in sample_ingredients:
#         canonical_name = inventory_db.canonicalize(ingredient["bottle_name"])
#         if canonical_name not in current_cache:
#             inventory_db.add_ingredient(
#                 bottle_name=ingredient["bottle_name"],
#                 type=ingredient["type"],
#                 category=ingredient["category"],
#                 abv=ingredient["abv"],
#                 unit=ingredient["unit"],
#                 quantity=ingredient["quantity"],
#                 is_open=ingredient["is_open"],
#                 curr_amount=ingredient["curr_amount"]
#             )
#         else:
#             print(f"Ingredient already exists: {canonical_name}")
#
#
# if __name__ == "__main__":
#     db = InventoryDB()
#     # For testing, you can import from JSON or load sample data.
#     # To import from JSON, uncomment the following line and ensure you have an ingredients.json file.
#     # db.import_from_json("ingredients.json")
#
#     # For sample data:
#     load_sample_data(db)
#     db.close()
