import sqlite3

DB_NAME = "database.db"

android_id = input("Enter Android ID: ").strip()

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    cursor.execute(
        "INSERT INTO licenses (android_id) VALUES (?)",
        (android_id,)
    )
    conn.commit()
    print("ID added successfully")
except sqlite3.IntegrityError:
    print("This ID already exists")
finally:
    conn.close()
