import json
import sqlite3

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#not using this anymore, have better func in inventory_db.pu
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Load JSON data into a Python dictionary.
with open('bar_inventory.json', 'r', encoding='utf-8') as file:
    cocktails_data = json.load(file)

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

    # Create the liquors table if it doesn't exist.
cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bottle_name TEXT NOT NULL,  -- The specific product name, e.g., "Tanqueray Gin"
            type TEXT NOT NULL,         -- The general type, e.g., "Gin", "Whiskey"
            category TEXT,              -- A broader category, e.g., "Spirit", "Liqueur"
            unit TEXT NOT NULL,         -- The measurement unit, e.g., "ml", "bottle"
            quantity REAL NOT NULL,     -- The amount available in that unit
            abv REAL,                   -- Alcohol by Volume percentage (optional)
            is_open INTEGER DEFAULT 1   -- 1 = Open, 0 = Unopened (Optional: Tracks if the bottle is opened)
            curr_amount REAL            -- if later i want it to reduce after making something
);

    ''')



    # Here, we are setting default values for the other columns.
    for name in liquor_names:
        cursor.execute('''
            INSERT INTO inventory (name, category, abv, unit, curr_amount, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, None, None, None, 0, 0))

    # Commit the changes and close the connection.
    conn.commit()
    conn.close()
    print("Liquors inserted successfully.")


