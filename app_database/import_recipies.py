import json
import sqlite3

# Load JSON data into a Python dictionary.
with open('cocktail_book.json', 'r', encoding='utf-8') as file:
    cocktails_data = json.load(file)

# Connect to (or create) the SQLite database.
conn = sqlite3.connect('cocktails.db')
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
  prep_method TEXT,
  made_from TEXT,
  flavor TEXT,
  glass_type TEXT,
  garnish TEXT
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
    prep_method = recipe.get("method")
    made_from = recipe.get("made_from")
    flavor = recipe.get("flavor", None)  # TODO delete the none after all has
    glass_type = recipe.get("glass_type", None)
    garnish = recipe.get("garnish", None)

    # Insert the recipe into the table.
    cursor.execute('''
   INSERT INTO cocktails (name, abv, is_easy_to_make, ingredients, instructions, personal_notes, 
                           is_favorite, times_made, prep_method, made_from, flavor, glass_type, garnish)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, abv, is_easy_to_make, ingredients, instructions, personal_notes,
          is_favorite, times_made, prep_method, made_from, flavor, glass_type, garnish))

# Commit the changes and close the connection.
conn.commit()
conn.close()

print("Cocktail recipes have been successfully imported.")
