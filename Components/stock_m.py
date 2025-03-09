from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
    QComboBox, QDateEdit, QGridLayout, QMessageBox, QSizePolicy, QHeaderView,QInputDialog
)
import sqlite3
import sys
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt
from Categories import CategoryPage


class StockManagementPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Management System")
        self.setGeometry(100, 100, 1200, 600)

        # Database Connection
        self.connection = sqlite3.connect("restaurant_management.db")
        self.cursor = self.connection.cursor()

        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.setObjectName("main_layout")  # Main layout ID

        # Frame 1 (Input Fields & Buttons)
        frame1 = QWidget()
        frame1.setObjectName("frame1")  # Frame 1 ID
        frame1_layout = QGridLayout()
        frame1.setLayout(frame1_layout)

        self.category_input = QComboBox()
        self.category_input.setObjectName("category_input")  # Category Input ID
        self.populate_categories()

        self.quantity_input = QLineEdit()
        self.quantity_input.setObjectName("quantity_input")  # Quantity Input ID
        self.quantity_input.setPlaceholderText("Quantity")

        self.unit_input = QLineEdit()
        self.unit_input.setObjectName("unit_input")  # Unit Input ID
        self.unit_input.setPlaceholderText("Unit (e.g., kg, pcs)")
        self.Low_SA_input = QLineEdit()
        self.Low_SA_input.setObjectName("Low_SA_input")  # Low Stock Alert Input ID
        self.Low_SA_input.setPlaceholderText("e.g.5,10")

        current_date = QDate.currentDate()
        self.purchase_date_input = QDateEdit()
        self.purchase_date_input.setDate(current_date)
        self.purchase_date_input.setObjectName("purchase_date_input")  # Purchase Date Input ID

        self.expiry_date_input = QDateEdit()
        self.expiry_date_input.setDate(current_date.addDays(10))
        self.expiry_date_input.setObjectName("expiry_date_input")  # Expiry Date Input ID

        # Add input fields to Frame 1

        frame1_layout.addWidget(QLabel("Category:"), 1, 0)
        frame1_layout.addWidget(self.category_input, 1, 1)
        frame1_layout.addWidget(QLabel("Quantity:"), 2, 0)
        frame1_layout.addWidget(self.quantity_input, 2, 1)
        frame1_layout.addWidget(QLabel("Unit:"), 3, 0)
        frame1_layout.addWidget(self.unit_input, 3, 1)
        frame1_layout.addWidget(QLabel("Low Stock Alert:"), 4, 0)
        frame1_layout.addWidget(self.Low_SA_input, 4, 1)
        frame1_layout.addWidget(QLabel("Purchase Date:"), 5, 0)
        frame1_layout.addWidget(self.purchase_date_input, 5, 1)
        frame1_layout.addWidget(QLabel("Expiry Date:"), 6, 0)
        frame1_layout.addWidget(self.expiry_date_input, 6, 1)

        # Buttons (Two Rows)
        self.add_button = QPushButton("Add Stock")
        self.add_button.setObjectName("add_button")  # Add Stock Button ID
        self.update_button = QPushButton("Update Stock")
        self.update_button.setObjectName("update_button")  # Update Stock Button ID
        self.delete_button = QPushButton("Delete Stock")
        self.delete_button.setObjectName("delete_button")  # Delete Stock Button ID
        self.clear_button = QPushButton("Clear Fields")
        self.clear_button.setObjectName("clear_button")  # Clear Fields Button ID

        # Add button functionality
        self.add_button.clicked.connect(self.add_stock)
        self.update_button.clicked.connect(self.update_stock)
        self.delete_button.clicked.connect(self.delete_stock)
        self.clear_button.clicked.connect(self.clear_fields)

        # Add buttons to Frame 1
        frame1_layout.addWidget(self.add_button, 7, 0)
        frame1_layout.addWidget(self.update_button, 7, 1)
        frame1_layout.addWidget(self.delete_button, 8, 0)
        frame1_layout.addWidget(self.clear_button, 8, 1)

        # Frame 2 (Table & Search)
        frame2 = QWidget()
        frame2.setObjectName("frame2")  # Frame 2 ID
        frame2_layout = QVBoxLayout()
        frame2.setLayout(frame2_layout)


        # Search Section
        search_layout = QHBoxLayout()
        search_layout.setObjectName("search_layout")  # Search Layout ID
        self.filter_combo = QComboBox()
        self.filter_combo.setObjectName("filter_combo")  # Filter ComboBox ID
        self.filter_combo.addItems(["Select by: ID", "Product"])
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("search_bar")  # Search Bar ID
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("search_button")  # Search Button ID
        self.search_button.clicked.connect(self.search_stock)

        # Add search components
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        frame2_layout.addLayout(search_layout)
        #============ add low stock button ===============
        # Create the All Product button
        self.all_product_button = QPushButton("All Products")
        self.all_product_button.setObjectName("allProductButton")

        self.low_stock_button = QPushButton("Show Low Stock")
        self.low_stock_button.setObjectName("low_stock_button")  # Low Stock Button ID
       
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.low_stock_button)
        self.button_layout.addWidget(self.all_product_button)

        # Add the layout to the bottom section of Frame2 (where both buttons will appear)
        frame2_layout.addLayout(self.button_layout)

        # Connect the All Product button to a function that shows all products
        self.all_product_button.clicked.connect(self.show_all_products)
        self.low_stock_button.clicked.connect(self.show_low_stock)
        # frame2.setLayout(frame2_layout)

        # # Add low stock button
        # self.setup_low_stock_button(frame2_layout)

        # Stock Table
        self.stock_table = QTableWidget()
        self.stock_table.setObjectName("stock_table")  # Stock Table ID
        self.stock_table.setColumnCount(6)
        self.stock_table.setHorizontalHeaderLabels(
            ["ID", "Product ", "Quantity", "Unit", "Purchase Date", "Expiry Date"]
        )
        self.stock_table.setSelectionBehavior(self.stock_table.SelectRows)
        self.stock_table.setSelectionMode(self.stock_table.SingleSelection)
        self.stock_table.itemSelectionChanged.connect(self.select_row)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch columns to fit the table width
        self.stock_table.setColumnWidth(4, 300)  # Set width of the "Purchase Date" column

        # Resize other columns based on their contents
        self.stock_table.resizeColumnsToContents()
        frame2_layout.addWidget(self.stock_table)
        self.refresh_table()


        # Add Frames to Main Layout
        main_layout.addWidget(frame1, 1)
        main_layout.addWidget(frame2, 2)

        # Set Main Layout
        container = QWidget()
        container.setObjectName("container")  # Container ID
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.load_stylesheet()

    def load_stylesheet(self):
        """Load the QSS stylesheet file to apply UI styles."""
        with open("Components/styles/stock.qss", "r") as f:
            self.setStyleSheet(f.read())

    def populate_categories(self):
        """Fetch and populate category ComboBox from the database."""
        self.category_input.clear()
        query = "SELECT name FROM category"
        self.cursor.execute(query)
        categories = self.cursor.fetchall()

        # Add categories to ComboBox
        self.category_input.addItem("Select Category")
        for category in categories:
            self.category_input.addItem(category[0])

        # Add 'Add Category' button as the last item
        self.category_input.addItem("Add New Category")
        self.category_input.currentIndexChanged.connect(self.handle_category_selection)


    def handle_category_selection(self, index):
        """Handle selection of 'Add New Category' from ComboBox."""
        if self.category_input.itemText(index) == "Add New Category":
            # Open the Category Page when "Add New Category" is selected
            self.add_category()

            # Reset the ComboBox to the default selection after opening the Category Page
            self.category_input.setCurrentIndex(0)


    def add_category(self):
        """Open the Category Page."""
        self.category = CategoryPage()  # Keep a reference to avoid garbage collection
        self.category.setWindowFlags(Qt.Window)
        self.category.show()



    def refresh_table(self):
        """Refresh the stock table with data from the database."""
        self.stock_table.setRowCount(0)
        query = "SELECT * FROM stock"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row_index, row_data in enumerate(rows):
            self.stock_table.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.stock_table.setItem(row_index, col_index, item)

            # Highlight rows with low stock
            quantity = int(row_data[2])  # Assuming quantity is in the 3rd column (index 2)
            low_stock_threshold = 10  # You can adjust or fetch this dynamically
            if quantity <= low_stock_threshold:
                for col_index in range(self.stock_table.columnCount()):
                    self.stock_table.item(row_index, col_index).setBackground(Qt.red)
    def show_all_products(self):
        # This function should display all the products in the table or any relevant section
        print("Displaying all products")
        # Example: You can refresh or update the table with all products here
        self.refresh_table()  # Assuming this is your method to update the table

    def show_low_stock(self):
        """Display only items with stock below the threshold."""
        self.stock_table.setRowCount(0)
        low_stock_threshold = 10  # Adjust as needed
        query = "SELECT * FROM stock WHERE quantity <= ?"
        self.cursor.execute(query, (low_stock_threshold,))
        rows = self.cursor.fetchall()
        for row_index, row_data in enumerate(rows):
            self.stock_table.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.stock_table.setItem(row_index, col_index, item)
                item.setBackground(Qt.red)

    def setup_low_stock_button(self, frame2_layout):
        """Add the 'Show Low Stock' button to the UI."""
        self.low_stock_button = QPushButton("Show Low Stock")
        self.low_stock_button.setObjectName("low_stock_button")  # Low Stock Button ID
        self.low_stock_button.clicked.connect(self.show_low_stock)
        frame2_layout.addWidget(self.low_stock_button)

    def select_row(self):
        """Populate fields when a stock item is selected for editing."""
        selected_row = self.stock_table.currentRow()
        if selected_row < 0:
            return  # No row selected

        stock_id = self.stock_table.item(selected_row, 0).text()
        category = self.stock_table.item(selected_row, 1).text()
        quantity = self.stock_table.item(selected_row, 2).text()
        unit = self.stock_table.item(selected_row, 3).text()
        purchase_date = self.stock_table.item(selected_row, 4).text()
        expiry_date = self.stock_table.item(selected_row, 5).text()

     
        self.category_input.setCurrentText(category)
        self.quantity_input.setText(quantity)
        self.unit_input.setText(unit)
        self.purchase_date_input.setDate(QDate.fromString(purchase_date, "yyyy-MM-dd"))
        self.expiry_date_input.setDate(QDate.fromString(expiry_date, "yyyy-MM-dd"))

        self.category_input.setDisabled(False)
        self.quantity_input.setReadOnly(False)
        self.unit_input.setReadOnly(False)
        self.purchase_date_input.setDisabled(False)
        self.expiry_date_input.setDisabled(False)


    def add_stock(self):
        """Add a new stock item to the database with validation."""
        category = self.category_input.currentText()
        quantity = self.quantity_input.text()
        unit = self.unit_input.text()
        purchase_date = self.purchase_date_input.date().toString("yyyy-MM-dd")
        expiry_date = self.expiry_date_input.date().toString("yyyy-MM-dd")

        # Validation
        if not category or not quantity or not unit:
            QMessageBox.warning(self, "Validation Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Quantity must be a number!")
            return

        # Check if the category already exists in the database
        query_check = "SELECT COUNT(*) FROM stock WHERE category = ?"
        self.cursor.execute(query_check, (category,))
        result = self.cursor.fetchone()

        if result[0] > 0:
            QMessageBox.warning(self, "Duplicate Category", f"The category '{category}' already exists in the stock table!")
            return

        # Insert into database if the category does not exist
        query_insert = """
        INSERT INTO stock (category, quantity, unit, purchase_date, expiry_date)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query_insert, (category, quantity, unit, purchase_date, expiry_date))
        self.connection.commit()
        QMessageBox.information(self, "Success", "Stock item added successfully!")
        self.clear_fields()
        self.refresh_table()

    def update_stock(self):
        """Update an existing stock item with validation."""
        selected_row = self.stock_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a row to update!")
            return

        stock_id = self.stock_table.item(selected_row, 0).text()
  
        category = self.category_input.currentText()
        quantity = self.quantity_input.text()
        unit = self.unit_input.text()
        purchase_date = self.purchase_date_input.date().toString("yyyy-MM-dd")
        expiry_date = self.expiry_date_input.date().toString("yyyy-MM-dd")

        # Validation
        if not category or not quantity or not unit:
            QMessageBox.warning(self, "Validation Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Quantity must be a number!")
            return

        # Update database
        query = """
        UPDATE stock
        SET  category = ?, quantity = ?, unit = ?, purchase_date = ?, expiry_date = ?
        WHERE id = ?
        """
        self.cursor.execute(query, (category, quantity, unit, purchase_date, expiry_date, stock_id))
        self.connection.commit()
        QMessageBox.information(self, "Success", "Stock item updated successfully!")
        self.clear_fields()
        self.refresh_table()

    def delete_stock(self):
        """Delete a selected stock item with confirmation."""
        selected_row = self.stock_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete!")
            return

        stock_id = self.stock_table.item(selected_row, 0).text()

        # Confirm deletion
        confirm = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this stock item?", 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            # Delete from database
            query = "DELETE FROM stock WHERE id = ?"
            self.cursor.execute(query, (stock_id,))
            self.connection.commit()
            QMessageBox.information(self, "Success", "Stock item deleted successfully!")
            self.clear_fields()
            self.refresh_table()

    def search_stock(self):
        """Search stock based on selected criteria."""
        filter_option = self.filter_combo.currentText()
        search_text = self.search_bar.text()

        if not search_text:
            QMessageBox.warning(self, "Search Error", "Please enter a search term!")
            return

        query = ""
        if filter_option == "Product":
            query = "SELECT * FROM stock WHERE category LIKE ?"
            params = ('%' + search_text + '%',)
    
        else:  # Default to ID search
            try:
                search_id = int(search_text)
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "ID must be a number!")
                return
            query = "SELECT * FROM stock WHERE id = ?"
            params = (search_id,)

        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            self.stock_table.setRowCount(0)
            if not rows:
                QMessageBox.information(self, "No Results", "No stock items match the search criteria.")
            else:
                for row_index, row_data in enumerate(rows):
                    self.stock_table.insertRow(row_index)
                    for col_index, col_data in enumerate(row_data):
                        self.stock_table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while searching:\n{str(e)}")


    def clear_fields(self):
        """Clear all input fields."""
      
        self.category_input.setCurrentIndex(0)
        self.quantity_input.clear()
        self.unit_input.clear()
        self.Low_SA_input.clear()
    # Set purchase date to today
        current_date = QDate.currentDate()
        self.purchase_date_input.setDate(current_date)

        # Set expiry date to 10 days from today
        expiry_date = current_date.addDays(10)
        self.expiry_date_input.setDate(expiry_date)



        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockManagementPage()
    window.show()
    sys.exit(app.exec_())
