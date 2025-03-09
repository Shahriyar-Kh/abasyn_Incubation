import sqlite3

# Connect to your SQLite database (change the path to your db file)
conn = sqlite3.connect('restaurant_management.db')
cursor = conn.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    print(table[0])


cursor.execute("DROP TABLE IF EXISTS suppliers;")
conn.commit()  # Commit the changes
print("Table deleted successfully")
cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

# # Retrieve all data from the orders table
# cursor.execute("SELECT * FROM order_items")

# # Fetch all results
# orders = cursor.fetchall()

# # Print all orders
# for order in orders:
#     print(order)



conn.close()
