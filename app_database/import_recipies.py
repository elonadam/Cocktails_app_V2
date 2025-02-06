import json
import sqlite3


# Load JSON data into a Python dictionary.
with open('cocktail_book.json','r', encoding='utf-8') as file:
    cocktails_data = json.load(file)

# Connect to (or create) the SQLite database.
conn = sqlite3.connect('venv/cocktails.db')
cursor = conn.cursor()

# Create the cocktails table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS cocktails (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  abv REAL,
  is_easy_to_make INTEGER,
  ingredients TEXT,
  instructions TEXT,
  personal_notes TEXT,
  is_favorite INTEGER,
  times_made INTEGER,
  method TEXT,
  need_to_make TEXT
)
''')

# Prepare to insert data from JSON into the table.
for key, recipe in cocktails_data.items():
    # Extract fields from each recipe.
    name = recipe.get("name")
    abv = recipe.get("abv")
    is_easy_to_make = 1 if recipe.get("is_easy_to_make", False) else 0
    # Convert the list of ingredients to a JSON string.
    ingredients = json.dumps(recipe.get("ingredients", []))
    instructions = recipe.get("instructions")
    personal_notes = recipe.get("personal_notes")
    is_favorite = 1 if recipe.get("is_favorite", False) else 0
    times_made = recipe.get("times_made", 0)
    method = recipe.get("method")
    # 'need_to_make' is optional; use None if not provided.
    need_to_make = recipe.get("need_to_make", None)

    # Insert the recipe into the table.
    cursor.execute('''
    INSERT INTO cocktails (name, abv, is_easy_to_make, ingredients, instructions, personal_notes, is_favorite, times_made, method, need_to_make)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, abv, is_easy_to_make, ingredients, instructions, personal_notes, is_favorite, times_made, method, need_to_make))

# Commit the changes and close the connection.
conn.commit()
conn.close()

print("Cocktail recipes have been successfully imported.")
