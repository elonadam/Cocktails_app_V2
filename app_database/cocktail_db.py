import sqlite3
import json

# i updated this using 4o and "import_reci" files, may not work 10.2.25
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
                is_easy_to_make INTEGER,  -- 0 for False, 1 for True
                ingredients TEXT,         -- JSON string storing the list of ingredients
                instructions TEXT,
                personal_notes TEXT,
                is_favorite INTEGER,      -- 0 for False, 1 for True
                times_made INTEGER,
                prep_method TEXT,
                made_from TEXT,           -- Optional field; can be NULL
                flavor TEXT,
                glass_type TEXT,
                garnish TEXT
            )
        ''')
        self.connection.commit()

    def load_cache(self):
        """Load cocktail data from the database into the cache."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT id, name, abv, is_easy_to_make, ingredients, instructions, personal_notes, 
                   is_favorite, times_made, prep_method, made_from, flavor, glass_type, garnish
            FROM cocktails
        ''')
        rows = cursor.fetchall()
        self.cache = {}
        for row in rows:
            (id, name, abv, is_easy_to_make, ingredients, instructions, personal_notes,
             is_favorite, times_made, prep_method, made_from, flavor, glass_type, garnish) = row
            self.cache[name] = {
                'id': id,
                'name': name,
                'abv': abv,
                'is_easy_to_make': is_easy_to_make,
                'ingredients': json.loads(ingredients),  # Convert JSON string back to a list
                'instructions': instructions,
                'personal_notes': personal_notes,
                'is_favorite': is_favorite,
                'times_made': times_made,
                'prep_method': prep_method,
                'made_from': made_from,
                'flavor': flavor,
                'glass_type': glass_type,
                'garnish': garnish
            }
        return self.cache

    def add_cocktail(self, name, abv, is_easy_to_make, ingredients, instructions, personal_notes,
                     is_favorite, times_made, prep_method, made_from, flavor, glass_type, garnish):
        ingredients_json = json.dumps(ingredients)
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO cocktails (name, abv, is_easy_to_make, ingredients, instructions, personal_notes, 
                                   is_favorite, times_made, prep_method, made_from, flavor, glass_type, garnish)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, abv, is_easy_to_make, ingredients_json, instructions, personal_notes,
              is_favorite, times_made, prep_method, made_from, flavor, glass_type, garnish))
        self.connection.commit()
        # Update the in-memory cache.
        self.cache[name] = {
            'abv': abv,
            'is_easy_to_make': is_easy_to_make,
            'ingredients': ingredients,
            'instructions': instructions,
            'personal_notes': personal_notes,
            'is_favorite': is_favorite,
            'times_made': times_made,
            'prep_method': prep_method,
            'made_from': made_from,
            'flavor': flavor,
            'glass_type': glass_type,
            'garnish': garnish
        }

    def close(self):
        self.connection.close()
