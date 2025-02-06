import sqlite3
import json


class CocktailDB:
    def __init__(self, db_path='cocktails.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_tables()
        self.cache = {}  # This dictionary holds the cocktail data for fast lookups.

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                abv REAL,
                glass_type TEXT,
                garnish TEXT,
                is_easy_to_make INTEGER,  -- 0 for False, 1 for True
                ingredients TEXT,         -- JSON string storing the list of ingredients
                instructions TEXT,
                personal_notes TEXT,
                is_favorite INTEGER,      -- 0 for False, 1 for True
                times_made INTEGER,
                method TEXT,
                need_to_make TEXT         -- Optional field; can be NULL
            )
        ''')
        self.connection.commit()

    def load_cache(self):
        """Load cocktail data from the database into the cache."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT name, abv, preparation_method, glass_type, garnish, ingredients FROM cocktails')
        rows = cursor.fetchall()
        self.cache = {}
        for row in rows:
            name, abv, prep_method, glass, garnish, ingredients = row
            self.cache[name] = {
                'abv': abv,
                'preparation_method': prep_method,
                'glass_type': glass,
                'garnish': garnish,
                'ingredients': json.loads(ingredients)  # Convert JSON string back to a dict
            }
        return self.cache

    def add_cocktail(self, name, abv, prep_method, glass, garnish, ingredients):
        ingredients_json = json.dumps(ingredients)
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO cocktails (name, abv, preparation_method, glass_type, garnish, ingredients)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, abv, prep_method, glass, garnish, ingredients_json))
        self.connection.commit()
        # Update the in-memory cache.
        self.cache[name] = {
            'abv': abv,
            'preparation_method': prep_method,
            'glass_type': glass,
            'garnish': garnish,
            'ingredients': ingredients
        }

    def close(self):
        self.connection.close()
