import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,QMessageBox, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QFrame, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sqlite3

# Connect to the database
conn = sqlite3.connect('restaurant_management.db')
cursor = conn.cursor()


class ProductManagementUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Management System")
        self.setGeometry(100, 100, 1600, 900)
        
        # Main layout
        main_layout = QVBoxLayout()

        # Create Frames
        frame1 = QFrame()
        frame2 = QFrame()
        frame3 = QFrame()

        # Layout for product details and CRUD buttons (Frame1)
        frame1_layout = QFormLayout()
        self.product_name_input = QLineEdit()
        self.product_category_input = QComboBox()
        self.product_category_input.addItems(['Chicken', 'Mutton', 'Drink', 'Salad', 'Tea'])
        self.product_price_input = QLineEdit()
        self.product_quantity_input = QLineEdit()
        self.product_status_input = QComboBox()
        self.product_status_input.addItems(['available', 'out_of_stock'])

        self.add_button = QPushButton("Add Product")
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_product)

        self.update_button = QPushButton("Update Product")
        self.update_button.setObjectName("update_button")
        self.update_button.clicked.connect(self.update_product)

        self.delete_button = QPushButton("Delete Product")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_product)

        self.clear_button = QPushButton("Clear Fields")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.clicked.connect(self.clear_fields)


        frame1_layout.addRow(QLabel("Product Name:"), self.product_name_input)
        frame1_layout.addRow(QLabel("Product Category:"), self.product_category_input)
        frame1_layout.addRow(QLabel("Product Price:"), self.product_price_input)
        frame1_layout.addRow(QLabel("Product Quantity:"), self.product_quantity_input)
        frame1_layout.addRow(QLabel("Product Status:"), self.product_status_input)
        frame1_layout.addRow(self.add_button, self.update_button)
        frame1_layout.addRow(self.delete_button,self.clear_button)

        frame1.setLayout(frame1_layout)
        frame1.setObjectName("frame1")

        # Layout for product table (Frame2)
        frame2_layout = QVBoxLayout()
        self.product_table = QTableWidget()
        self.product_table.setObjectName("product_table")
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Quantity", "Status"])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
         # Connect the row click event to populate the fields
        self.product_table.cellClicked.connect(self.populate_fields_on_click)
        self.load_products()

        frame2_layout.addWidget(self.product_table)
        frame2.setLayout(frame2_layout)
        frame2.setObjectName("frame2")

        # Layout for product search (Frame3)
        frame3_layout = QHBoxLayout()
        self.search_field = QComboBox()
        self.search_field.addItems(['Select by Product_ID', 'Select by Name', 'Select by Category'])
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.search_product)

        frame3_layout.addWidget(QLabel("Search:"))
        frame3_layout.addWidget(self.search_field)
        frame3_layout.addWidget(self.search_input)
        frame3_layout.addWidget(self.search_button)

        frame3.setLayout(frame3_layout)
        frame3.setObjectName("frame3")

        # Set up the main layout (frame1 + frame2 side by side, frame3 on top of frame2)
        main_layout.addWidget(frame3)
        h_layout = QHBoxLayout()
        h_layout.addWidget(frame1)
        h_layout.addWidget(frame2)
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)
        self.setObjectName("main_window")

        self.apply_stylesheet()  # Load QSS Stylesheet
        self.clear_fields()


    def apply_stylesheet(self):
        """Load QSS Stylesheet."""
        try:
            with open("Components/styles/Product.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Stylesheet file 'employee_page.qss' not found!")
   
    def load_products(self):
        """Load products from the database and display them in the table."""
        # Clear the table before loading new data
        self.product_table.setRowCount(0)

        # Execute the query to fetch product data from the database
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        # Populate the table with fetched data
        for product in products:
            row_position = self.product_table.rowCount()
            self.product_table.insertRow(row_position)

            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                # Make the item read-only
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.product_table.setItem(row_position, col, item)

        # Disable selection for editing in the entire table
        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)


    def add_product(self):
        """Add a new product to the database with validation and duplicate checks."""
        # Get values from input fields
        name = self.product_name_input.text().strip()
        category = self.product_category_input.currentText()
        price = self.product_price_input.text().strip()
        quantity = self.product_quantity_input.text().strip()
        status = self.product_status_input.currentText()
        # Validate required fields
        missing_fields = []
        if not name:
            missing_fields.append(self.product_name_input)
        if not category:
            missing_fields.append(self.product_category_input)
        if not price:
            missing_fields.append(self.product_price_input)
        if not quantity:
            missing_fields.append(self.product_quantity_input)
        if not status:
            missing_fields.append(self.product_status_input)

        if missing_fields:
            for field in missing_fields:
                field.setStyleSheet("border: 2px solid red;")
            QMessageBox.warning(self, "Input Error", "Some required fields are missing!")
            return

        try:
            # Check if the product name already exists
            cursor.execute("SELECT COUNT(*) FROM products WHERE name = ?", (name,))
            product_exists = cursor.fetchone()[0] > 0

            if product_exists:
                QMessageBox.warning(self, "Duplicate Error", "Product already added!")
            else:
                # Insert new product into the database
                cursor.execute(
                    "INSERT INTO products (name, category, price, quantity, status) VALUES (?, ?, ?, ?, ?)",
                    (name, category, price, quantity, status)
                )
                conn.commit()
                self.load_products()
                QMessageBox.information(self, "Success", "Product successfully added!")

                # Clear the input fields
                self.clear_inputs()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add product: {str(e)}")
        self.clear_fields()

    def update_product(self):
        """Update an existing product in the database and show updated fields."""
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            product_id = self.product_table.item(selected_row, 0).text()
            
            # Get original values from the table
            original_name = self.product_table.item(selected_row, 1).text()
            original_category = self.product_table.item(selected_row, 2).text()
            original_price = self.product_table.item(selected_row, 3).text()
            original_quantity = self.product_table.item(selected_row, 4).text()
            original_status = self.product_table.item(selected_row, 5).text()
            
            # Get new input values
            name = self.product_name_input.text().strip()
            category = self.product_category_input.currentText().strip()
            price = self.product_price_input.text().strip()
            quantity = self.product_quantity_input.text().strip()
            status = self.product_status_input.currentText().strip()
            
            # Track updated fields
            updated_fields = []
            if name != original_name:
                updated_fields.append(f"Name: {original_name} → {name}")
            if category != original_category:
                updated_fields.append(f"Category: {original_category} → {category}")
            if price != original_price:
                updated_fields.append(f"Price: {original_price} → {price}")
            if quantity != original_quantity:
                updated_fields.append(f"Quantity: {original_quantity} → {quantity}")
            if status != original_status:
                updated_fields.append(f"Status: {original_status} → {status}")
            
            # Perform the update only if there are changes
            if updated_fields:
                try:
                    cursor.execute(
                        "UPDATE products SET name = ?, category = ?, price = ?, quantity = ?, status = ? WHERE product_id = ?",
                        (name, category, price, quantity, status, product_id)
                    )
                    conn.commit()
                    self.load_products()
                    
                    # Show updated fields in a message box
                    updated_fields_message = "\n".join(updated_fields)
                    QMessageBox.information(self, "Update Successful", f"The following fields were updated:\n\n{updated_fields_message}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update product: {str(e)}")
            else:
                QMessageBox.information(self, "No Changes", "No fields were updated.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a product to update.")
        self.clear_fields()


    def delete_product(self):
        """Delete the selected product from the database with confirmation and success messages."""
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            # Get the product details for confirmation
            product_id = self.product_table.item(selected_row, 0).text()
            product_name = self.product_table.item(selected_row, 1).text()
            
            # Show confirmation message box
            reply = QMessageBox.question(
                self, 
                "Delete Confirmation", 
                f"Are you sure you want to delete the product '{product_name}' (ID: {product_id})?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    # Perform the deletion
                    cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
                    conn.commit()
                    self.load_products()
                    
                    # Show success message
                    QMessageBox.information(self, "Deletion Successful", f"Product '{product_name}' has been successfully deleted.")
                except Exception as e:
                    # Handle errors
                    QMessageBox.critical(self, "Error", f"Failed to delete product: {str(e)}")
                self.clear_fields()

    # Define the reset/clear function
    def clear_fields(self):
        # Reset all fields to their default values
        self.product_name_input.clear()  # Clear product name field
        self.product_category_input.setCurrentIndex(0)  # Set category to first option (default)
        self.product_price_input.clear()  # Clear price field
        self.product_quantity_input.clear()  # Clear quantity field
        self.product_status_input.setCurrentIndex(0)  # Set status to first option (default)
    def search_product(self):
        """Search for a product based on user input."""
        search_term = self.search_input.text()
        search_field = self.search_field.currentText()
        
        self.product_table.setRowCount(0)  # Clear the table
        
        if search_field == 'Select by Product_ID':
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (search_term,))
        elif search_field == 'Select by Name':
            cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
        elif search_field == 'Select by Category':
            cursor.execute("SELECT * FROM products WHERE category LIKE ?", ('%' + search_term + '%',))
        
        products = cursor.fetchall()

        for product in products:
            row_position = self.product_table.rowCount()
            self.product_table.insertRow(row_position)
            for col, value in enumerate(product):
                self.product_table.setItem(row_position, col, QTableWidgetItem(str(value)))

     # Add the method to populate the fields when a row is clicked
    def populate_fields_on_click(self, row, column):
            """Populate fields with data from the selected row."""
            # Retrieve the item from the selected row
            product_name_item = self.product_table.item(row, 1)
            product_category_item = self.product_table.item(row, 2)
            product_price_item = self.product_table.item(row, 3)
            product_quantity_item = self.product_table.item(row, 4)
            product_status_item = self.product_table.item(row, 5)

            # Check if the items exist and retrieve their text, otherwise set as empty string
            product_name = product_name_item.text() if product_name_item else ""
            product_category = product_category_item.text() if product_category_item else ""
            product_price = product_price_item.text() if product_price_item else ""
            product_quantity = product_quantity_item.text() if product_quantity_item else ""
            product_status = product_status_item.text() if product_status_item else ""

            # Set the values in the fields
            self.product_name_input.setText(product_name)
            self.product_category_input.setCurrentText(product_category)
            self.product_price_input.setText(product_price)
            self.product_quantity_input.setText(product_quantity)
            self.product_status_input.setCurrentText(product_status)
  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProductManagementUI()
    window.show()
    sys.exit(app.exec_())
