import sqlite3
# Connect to SQLite database or create a new one
conn = sqlite3.connect("restaurant_management.db")
cursor = conn.cursor()

# Step 1: Create `users` table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT CHECK(role IN ('admin', 'manager', 'staff')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
)
''')

# Step 2: Create `employees` table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    address TEXT,
    position TEXT CHECK(position IN ('chef', 'waiter', 'manager', 'cleaner')) NOT NULL,
    salary REAL NOT NULL,
    hire_date DATE NOT NULL,
    status TEXT CHECK(status IN ('active', 'inactive')) DEFAULT 'active',
    id_card TEXT UNIQUE NOT NULL,
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Ensure the 'products' table is created with the correct schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT CHECK(status IN ('available', 'out_of_stock')) DEFAULT 'available'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    customer_address TEXT NOT NULL,
    table_number INTEGER NULL DEFAULT 0,
    delivery TEXT CHECK(delivery IN ('Yes', 'No')) DEFAULT 'No',
    current_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('Paid', 'Unpaid')) DEFAULT 'Unpaid',
    total_price Float NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    item_name TEXT,
    quantity INTEGER,
    price REAL,
    total REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
               ''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    order_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('Paid', 'Unpaid')) DEFAULT 'Unpaid',
    total_price FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
''')



# Step 6: Create `suppliers` and `supplies` tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT NOT NULL,
    address TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Purchase (
    Purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    product_category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    Purchase DATE NOT NULL,
    Total_price FLOAT NOT NULL,
    Unit_price FLOAT NOT NULL,        
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (stock_id) REFERENCES stock(id)
)
''')

# Step 8: Create `stock` table
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit TEXT NOT NULL,
    purchase_date DATE NOT NULL,
    expiry_date DATE,
    low_stock_threshold INTEGER NOT NULL DEFAULT 10,
    FOREIGN KEY (id) REFERENCES category(id)
               
)
''')
cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

# Step 7: Create `sales` table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    sale_date DATE DEFAULT CURRENT_DATE,
    total_amount REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
''')
# Commit changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully!")
