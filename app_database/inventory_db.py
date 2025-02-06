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

    def load_cache(self):
        """Load all ingredients from the database into the cache."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT name, quantity, unit, category FROM ingredients')
        rows = cursor.fetchall()
        # Create a dictionary where key is the ingredient name.
        self.cache = {
            row[0]: {'quantity': row[1], 'unit': row[2], 'category': row[3]}
            for row in rows
        }
        return self.cache

    def add_ingredient(self, name, quantity, unit, category):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO ingredients (name, quantity, unit, category) 
            VALUES (?, ?, ?, ?)
        ''', (name, quantity, unit, category))
        self.connection.commit()
        # Update the cache with the new ingredient.
        self.cache[name] = {'quantity': quantity, 'unit': unit, 'category': category}

    def update_ingredient(self, name, quantity):
        cursor = self.connection.cursor()
        cursor.execute('UPDATE ingredients SET quantity=? WHERE name=?', (quantity, name))
        self.connection.commit()
        # Update the in-memory cache.
        if name in self.cache:
            self.cache[name]['quantity'] = quantity

    def close(self):
        self.connection.close()
