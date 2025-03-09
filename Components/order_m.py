import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox,QMessageBox,QTextEdit,QHeaderView,QSizePolicy,
    QLabel, QPushButton, QFrame, QLineEdit, QDialog, QFormLayout, QWidget, QScrollArea, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtCore import Qt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.receipt_generator import generate_receipt



class AddToCartDialog(QDialog):
    def __init__(self, item, price, parent=None):
        super().__init__(parent)
        self.item = item
        self.price = price
        self.setWindowTitle(self.item)  # Set dialog title to the item name
        self.quantity = 0
        self.initUI()
        

    def initUI(self):
        layout = QVBoxLayout()

        # Quantity Input
        form_layout = QFormLayout()
        quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        form_layout.addRow(quantity_label, self.quantity_input)

        # Add Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add to Cart")
        cancel_button = QPushButton("Cancel")

        add_button.clicked.connect(self.add_to_cart)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        quantity_label.setObjectName("quantity_label")
        self.quantity_input.setObjectName("quantity_input")
        add_button.setObjectName("add_button")
        cancel_button.setObjectName("cancel_button")

    def add_to_cart(self):
        quantity = self.quantity_input.text()
        if not quantity.isdigit() or int(quantity) <= 0:
            QLabel("Invalid Quantity").show()
            return
        self.quantity = int(quantity)
        self.accept()



class OrderManagementPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("restaurant_management.db")
        self.cursor = self.conn.cursor()
        self.setWindowTitle("Order Management")
        self.setGeometry(100, 100, 1200, 800)
        self.cart_items = []
        self.initUI()

    def initUI(self):
        # Main Widget and Layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Top Section (Fixed Height 100px)
        top_frame = QFrame()
        top_frame.setFixedHeight(100)
        top_frame.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        top_layout = QHBoxLayout(top_frame)

        self.restaurant_label = QLabel("Restaurant Name")
        self.restaurant_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.order_management_label = QLabel("Order Management")
        self.date_label = QLabel()
        self.time_label = QLabel()


        top_layout.addWidget(self.restaurant_label)
        top_layout.addStretch()
        top_layout.addWidget(self.order_management_label)
        top_layout.addStretch()
        top_layout.addWidget(self.date_label)
        top_layout.addWidget(self.time_label)
        

        main_layout.addWidget(top_frame)

        # Initialize current_datetime_label in customer details frame
        self.current_datetime_label = QLabel()

        # Update real-time clock
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)
        self.update_datetime()
#++++++++++++++++ Top Saction IDS ++++++++++++++++++++++++++++
        top_frame.setObjectName("top_frame")
        self.restaurant_label.setObjectName("restaurant_label")
        self.order_management_label.setObjectName("order_management_label")
        self.date_label.setObjectName("date_label")
        self.time_label.setObjectName("time_label")

#=================== Main Section with 3 Frames=================================
        main_frame_layout = QHBoxLayout()

        # Frame 1: Menu (Double Width of Frame 2 and Frame 3)


        self.menu_frame = QFrame()
        self.menu_layout = QVBoxLayout()
        menu_label = QLabel("Menu")
        menu_label.setAlignment(Qt.AlignCenter)
        menu_label.setObjectName("menu_lebel")
        menu_label.setStyleSheet("background-color:black; color:white;")
        
        # Add the Menu Label to the layout
        self.menu_layout.addWidget(menu_label)
        self.menu_frame.setLayout(self.menu_layout)

        # Add a Scroll Area for Dynamic Menu
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        self.load_menu_items(scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        self.menu_layout.addWidget(scroll_area)
        main_frame_layout.addWidget(self.menu_frame, 3)
#++++++++++++++++++++++++++ Menu Saction ++++++++++++++++++++++
        self.menu_frame.setObjectName("menu_frame")
        scroll_area.setObjectName("menu_scroll_area")
        scroll_widget.setObjectName("menu_scroll_widget")

        # Frame 2: Cart
        self.cart_frame = QFrame()
        self.cart_frame.setStyleSheet("border: 1px solid black;")
        self.cart_layout = QVBoxLayout()
        self.cart_frame.setLayout(self.cart_layout)

        # Customer Inputs
        self.customer_details_frame = QFrame()
        self.customer_details_layout = QFormLayout(self.customer_details_frame)
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.table_input = QLineEdit()

        # Delivery dropdown with "Yes" or "No"
        self.delivery_input = QComboBox()
        self.delivery_input.addItems(["Yes", "No"])

        # Add customer details to the layout
        self.customer_details_layout.addRow("Name:", self.name_input)
        self.customer_details_layout.addRow("Phone:", self.phone_input)
        self.customer_details_layout.addRow("Address:", self.address_input)
        self.customer_details_layout.addRow("Table:", self.table_input)
        self.customer_details_layout.addRow("Delivery (Yes/No):", self.delivery_input)
        self.cart_layout.addWidget(self.customer_details_frame)

#======================= Cart Items and Total Price ===================================
        # Create a table to display cart items
        self.cart_items_table = QTableWidget()
        self.cart_items_table.setObjectName("cart_table")
        self.cart_items_table.setColumnCount(3)
        self.cart_items_table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Price"])

        self.cart_layout.addWidget(self.cart_items_table)

        self.total_price_label = QLabel("Total Price: $0.00")
        self.cart_layout.addWidget(self.cart_items_table)
        self.cart_layout.addWidget(self.total_price_label)

        self.cart_layout.addWidget(self.cart_frame)

        # Action Buttons
        self.action_buttons_frame = QFrame()
        self.action_buttons_layout = QHBoxLayout(self.action_buttons_frame)

        self.order_now_button = QPushButton("Order Now")
      
        self.clear_order_button = QPushButton("Clear Order")

        self.order_now_button.clicked.connect(self.place_order)
        
        self.clear_order_button.clicked.connect(self.clear_order)

        self.action_buttons_layout.addWidget(self.order_now_button)
        
        self.action_buttons_layout.addWidget(self.clear_order_button)

        self.cart_layout.addWidget(self.action_buttons_frame)

        # Adjust stretch factors to give more space to cart items
        self.cart_layout.setStretch(1, 4)  # Cart items frame gets more height
        self.cart_layout.setStretch(2, 1)  # Buttons frame gets less height

        main_frame_layout.addWidget(self.cart_frame, 1)
#++++++++++++++++++++++++++ Cart Frame ++++++++++++++++++++++++
        self.cart_frame.setObjectName("cart_frame")
        self.customer_details_frame.setObjectName("customer_details_frame")
        self.name_input.setObjectName("name_input")
        self.phone_input.setObjectName("phone_input")
        self.address_input.setObjectName("address_input")
        self.table_input.setObjectName("table_input")
        self.delivery_input.setObjectName("delivery_input")
        self.cart_frame.setObjectName("cart_frame")
       
        self.total_price_label.setObjectName("total_price_label")
        self.action_buttons_frame.setObjectName("action_buttons_frame")
        self.order_now_button.setObjectName("order_now_button")
        
        self.clear_order_button.setObjectName("delete_order_button")


#====================== Frame 3: Orders (Unpaid Orders List) ===========================
        self.orders_frame = QFrame()
        self.orders_frame.setStyleSheet("border: 1px solid black;")
        self.orders_frame.setFixedHeight(200)  # Set the height to your desired value (e.g., 200 pixels)
        self.orders_layout = QVBoxLayout(self.orders_frame)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["Order ID", "Customer Name", "Total Price", "Action"])
        self.orders_table.setSelectionMode(QTableWidget.SingleSelection)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch columns to fit the table width
        # Make all rows read-only by setting items' flags to prevent editing
        def make_rows_read_only():
            for row in range(self.orders_table.rowCount()):
                for col in range(self.orders_table.columnCount()):
                    item = self.orders_table.item(row, col)
                    if item:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Disable editing
#+++++++++++++++++++++++++++ order frame ========================
        self.orders_frame.setObjectName("orders_frame")
        self.orders_table.setObjectName("orders_table")

        # Load unpaid orders into the table
        self.load_unpaid_orders()
        make_rows_read_only()

        # Add the table to the orders layout
        self.orders_layout.addWidget(self.orders_table)

        # Add widgets and frames to main layout
        main_frame_layout.addWidget(self.orders_frame)  # Keep other widgets above it
        main_layout.addLayout(main_frame_layout)

        # Add the orders frame (cart) at the bottom of the main layout
        self.menu_layout.addWidget(self.orders_frame)

        # Load QSS File
        self.apply_stylesheet()

    def apply_stylesheet(self):
        """Load and apply the QSS file."""
        try:
            with open("Components/styles/order.qss", "r") as qss_file:
                self.setStyleSheet(qss_file.read())
        except FileNotFoundError:
            print("QSS file not found. Please ensure 'order.qss' is in the same directory.")
    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        self.date_label.setText(current_datetime.toString("yyyy-MM-dd"))
        self.time_label.setText(current_datetime.toString("hh:mm:ss"))
        if hasattr(self, 'current_datetime_label'):
            self.current_datetime_label.setText(current_datetime.toString("yyyy-MM-dd hh:mm:ss"))

    def load_menu_items(self, layout):
        # Query distinct categories
        categories = self.cursor.execute("SELECT DISTINCT category FROM products").fetchall()

        for category, in categories:
            category_label = QLabel(category)
            category_label.setObjectName("category")
            category_label.setAlignment(Qt.AlignCenter) 
            layout.addWidget(category_label)

            # Query products by category
            products = self.cursor.execute("SELECT name, price FROM products WHERE category = ?", (category,)).fetchall()

            # Create a Grid Layout for Products
            grid_layout = QGridLayout()
            row, col = 0, 0

            for name, price in products:
                btn = QPushButton(f"{name}\n${price}")
                btn.setObjectName("items_btn")
                btn.clicked.connect(lambda _, n=name, p=price: self.open_add_to_cart_dialog(n, p))
                grid_layout.addWidget(btn, row, col)

                # Adjust row and column for 3-column layout
                col += 1
                if col > 2:  # Move to the next row after 3 columns
                    col = 0
                    row += 1

            layout.addLayout(grid_layout)

    def open_add_to_cart_dialog(self, item, price):
        dialog = AddToCartDialog(item, price, self)
        if dialog.exec_() == QDialog.Accepted:
            quantity = dialog.quantity
            total_price = quantity * price
            
            # Check if the item already exists in the cart
            for idx, (existing_item, existing_quantity, existing_price, existing_total) in enumerate(self.cart_items):
                if existing_item == item:
                    # If item exists, update the quantity and total price
                    self.cart_items[idx] = (existing_item, existing_quantity + quantity, existing_price, (existing_quantity + quantity) * existing_price)
                    self.update_cart_display()
                    return

            # If the item is not found, add it to the cart
            self.cart_items.append((item, quantity, price, total_price))
            self.update_cart_display()


    def update_cart_display(self):
        # Update cart items table and total price
        self.cart_items_table.setRowCount(0)  # Clear existing rows
        total_price = 0
        for idx, (item, quantity, price, total) in enumerate(self.cart_items):
            row_position = self.cart_items_table.rowCount()
            self.cart_items_table.insertRow(row_position)

            # Set item name, quantity, and price
            self.cart_items_table.setItem(row_position, 0, QTableWidgetItem(item))  # Item Name
            self.cart_items_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))  # Quantity
            self.cart_items_table.setItem(row_position, 2, QTableWidgetItem(f"${total:.2f}"))  # Price
            
            total_price += total
        
        # Set the updated total price
        self.total_price_label.setText(f"Total Price: ${total_price:.2f}")



    def place_order(self):
        # Get customer details
        name = self.name_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        table = self.table_input.text()  # Table number or leave empty if no table
        delivery = self.delivery_input.currentText()  # "Yes" or "No" for delivery
        current_datetime = self.current_datetime_label.text()  # Current DateTime value
        total_price = sum([item[3] for item in self.cart_items])  # Sum the prices of items in the cart

        # Insert into orders table
        self.cursor.execute("""
            INSERT INTO orders (customer_name, customer_phone, customer_address, table_number, delivery, current_datetime, total_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, phone, address, table, delivery, current_datetime, total_price))  # 0 for unpaid
        self.conn.commit()

        # Get the last inserted order ID
        order_id = self.cursor.lastrowid

        # Insert cart items into the order_items table
        for item in self.cart_items:
            
            item_name=item[0]    
            quantity = item[1]    # Assuming item[2] is the quantity
            price = item[2]       # Assuming item[3] is the price per item
            totalprice = item[3]       # Assuming item[3] is the price per item
            
            self.cursor.execute("""
                INSERT INTO order_items (order_id,item_name,quantity,price,total)
                VALUES (?, ?, ?, ?,?)
            """, (order_id,item_name, quantity, price,totalprice))
        
        self.conn.commit()

        # Reset cart and customer details after placing the order
        self.cart_items = []
        self.update_cart_display()
        self.clear_customer_details()

        # Reload unpaid orders list
        self.load_unpaid_orders()


    def load_unpaid_orders(self):
        # Fetch unpaid orders from the database
        self.cursor.execute("SELECT * FROM orders WHERE status = 'Unpaid'")
        unpaid_orders = self.cursor.fetchall()

        # Clear existing rows in the table
        self.orders_table.setRowCount(0)

        if not unpaid_orders:  # No unpaid orders available
            row_position = self.orders_table.rowCount()
            self.orders_table.insertRow(row_position)
            empty_item = QTableWidgetItem("No unpaid orders available")
            self.orders_table.setItem(row_position, 0, empty_item)  # Add message in the first column
            self.orders_table.setSpan(row_position, 0, 1, 4)  # Span message across 4 columns
        else:
            for order in unpaid_orders:
                row_position = self.orders_table.rowCount()
                self.orders_table.insertRow(row_position)

                # Populate the table row with order details
                self.orders_table.setItem(row_position, 0, QTableWidgetItem(str(order[0])))  # Order ID
                self.orders_table.setItem(row_position, 1, QTableWidgetItem(order[1]))  # Customer Name
                self.orders_table.setItem(row_position, 2, QTableWidgetItem(f"${order[8]:.2f}"))  # Total Price

                # Create and configure the "Bill Now" button
                bill_button = QPushButton("Bill Now")
                bill_button.setObjectName("bill_now")
                bill_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                bill_button.clicked.connect(lambda checked, order_id=order[0]: self.generate_bill(order_id))
                self.orders_table.setCellWidget(row_position, 3, bill_button)


    def generate_bill(self, order_id):
        # Fetch order details from the database
        self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order = self.cursor.fetchone()

        if order:
            # Mark the order as paid
            self.cursor.execute("UPDATE orders SET status = 'Paid' WHERE order_id = ?", (order_id,))
            
            # Insert the paid order into the bills table
            self.cursor.execute("INSERT INTO bills (order_id, status, total_price) VALUES (?, ?, ?)",
                        (order_id, 'Paid', order[8]))
            self.conn.commit()
            
            
            # Retrieve order details
            customer_name = order[1]  # customer_name
            customer_phone = order[2]  # customer_phone
            customer_address = order[3]  # customer_address
            total_price = order[8]  # total_price
            table_number = order[4]  # table_number
            delivery = order[5]  # delivery

            # Fetch order items for the given order_id
            self.cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            order_items = self.cursor.fetchall()

            items = [{"item_name": item[2], "Quantity": item[3],"Price":item[4],"Total_price":item[5]} for item in order_items]
            print(items)
        # Call the generate_receipt function with the fetched values, including the items
            generate_receipt(order_id, customer_name, customer_phone, customer_address, total_price, table_number, delivery, items)
            # Reload unpaid orders
            self.load_unpaid_orders()



    def clear_order(self):
        # Clear cart items
        self.cart_items = []
        self.update_cart_display()

        # Clear customer details
        self.clear_customer_details()

        # Reset total price label
        self.total_price_label.setText("Total Price: $0.00")


    def clear_customer_details(self):
        # Assuming you have QLineEdit widgets for customer details
        self.name_input.clear()         # Clears the name field
        self.phone_input.clear()        # Clears the phone number field
        self.address_input.clear()      # Clears the address field
        self.table_input.clear()

        # If you have ComboBox widgets for customer-related details (e.g., selecting a city or a type)
        self.delivery_input.setCurrentIndex(0)  # Resets the city combo box to the first item (or any default item)

    def validate_fields(self):
    # Check if the customer name is empty
        if not self.customer_name_input.text():
            QMessageBox.warning(self, "Input Error", "Customer name is required!")
            return False

        # Ensure the cart is not empty (you can adjust this based on your cart implementation)
        if not self.get_cart_items():
            QMessageBox.warning(self, "Input Error", "Cart is empty!")
            return False

        return True


if __name__ == "__main__":
    app = QApplication([])
    
    window = OrderManagementPage()
    window.show()
    app.exec_()
   