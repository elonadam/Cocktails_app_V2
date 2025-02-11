#!/usr/bin/env python3
import sqlite3


def main():
    # Connect to (or create) the SQLite database file.
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create the liquors table if it doesn't exist.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            abv REAL,
            unit TEXT,
            curr_amount REAL,
            quantity INTEGER
        );
    ''')

    # List of liquors to be added.
    liquor_names = [
        "beefeater gin",
        "jack daniels whisky",
        "stoly vodka",
        "bolas triple sec",
        "lemon",
        "bolas blue curacao",
        "haymens sloe gin",
        "campari",
        "simple syrup",
        "rottan passionfruit syrup"
    ]

    # Insert each liquor into the table.
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


if __name__ == '__main__':
    main()
