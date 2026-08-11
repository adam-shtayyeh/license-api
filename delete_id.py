import sqlite3

DB_NAME = "database.db"

android_id = input("Enter Android ID to delete: ").strip()

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(
    "DELETE FROM licenses WHERE android_id = ?",
    (android_id,)
)

conn.commit()

if cursor.rowcount > 0:
    print("ID deleted successfully")
else:
    print("ID not found")

conn.close()