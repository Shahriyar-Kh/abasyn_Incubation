import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QDateEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
import sqlite3

class PurchaseManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Purchase Management System")
        self.setGeometry(100, 100, 1200, 700)
        self.conn = sqlite3.connect("restaurant_management.db")
        self.cursor = self.conn.cursor()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Purchase Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        # Supplier and Purchase Input Form
        form_layout = QHBoxLayout()

        # Supplier Details
        supplier_layout = QVBoxLayout()
        supplier_label = QLabel("Supplier Details")
        supplier_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        supplier_layout.addWidget(supplier_label)

        self.supplier_name_input = QLineEdit()
        self.supplier_name_input.setPlaceholderText("Supplier Name")
        supplier_layout.addWidget(self.supplier_name_input)

        self.supplier_contact_input = QLineEdit()
        self.supplier_contact_input.setPlaceholderText("Supplier Contact")
        supplier_layout.addWidget(self.supplier_contact_input)

        self.supplier_address_input = QLineEdit()
        self.supplier_address_input.setPlaceholderText("Supplier address")
        supplier_layout.addWidget(self.supplier_address_input)

        add_supplier_button = QPushButton("Add Supplier")
        add_supplier_button.clicked.connect(self.add_supplier)
        supplier_layout.addWidget(add_supplier_button)

        form_layout.addLayout(supplier_layout)

        # Purchase Details
        purchase_layout = QVBoxLayout()
        purchase_label = QLabel("Purchase Details")
        purchase_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        purchase_layout.addWidget(purchase_label)

        self.supplier_combo = QComboBox()
        self.load_suppliers()
        purchase_layout.addWidget(self.supplier_combo)

        self.category_combo = QComboBox()
        self.load_categories()
        purchase_layout.addWidget(self.category_combo)

        self.product_quantity_input = QLineEdit()
        self.product_quantity_input.setPlaceholderText("Quantity")
        self.product_quantity_input.setValidator(QDoubleValidator(0, 10000, 2))
        purchase_layout.addWidget(self.product_quantity_input)

        self.unit_price_input = QLineEdit()
        self.unit_price_input.setPlaceholderText("Unit Price")
        self.unit_price_input.setValidator(QDoubleValidator(0, 10000, 2))
        purchase_layout.addWidget(self.unit_price_input)

        self.purchase_date_input = QDateEdit()
        self.purchase_date_input.setCalendarPopup(True)
        purchase_layout.addWidget(self.purchase_date_input)

        add_purchase_button = QPushButton("Add Purchase")
        add_purchase_button.clicked.connect(self.add_purchase)
        purchase_layout.addWidget(add_purchase_button)

        form_layout.addLayout(purchase_layout)

        main_layout.addLayout(form_layout)

        # Purchase Table
        self.purchase_table = QTableWidget()
        self.purchase_table.setColumnCount(6)
        self.purchase_table.setHorizontalHeaderLabels(
            ["Supplier", "Category", "Quantity", "Unit Price", "Total Cost", "Purchase Date"]
        )
        main_layout.addWidget(self.purchase_table)

        # Main Widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Load purchase history
        self.load_purchases()

    def load_suppliers(self):
        """Load suppliers into the supplier combo box."""
        self.supplier_combo.clear()
        query = "SELECT supplier_id, name FROM suppliers"
        self.cursor.execute(query)
        suppliers = self.cursor.fetchall()
        for supplier in suppliers:
            self.supplier_combo.addItem(supplier[1], supplier[0])

    def load_categories(self):
        """Load categories into the category combo box."""
        self.category_combo.clear()
        query = "SELECT name FROM category"
        self.cursor.execute(query)
        categories = self.cursor.fetchall()
        for category in categories:
            self.category_combo.addItem(category[0])

    def load_purchases(self):
        """Load purchase history into the table."""
        query = """
        SELECT s.name, p.product_category, p.quantity, p.unit_price, p.total_price, p.purchase
        FROM Purchase p
        JOIN suppliers s ON p.supplier_id = s.supplier_id
        """
        self.cursor.execute(query)
        purchases = self.cursor.fetchall()

        self.purchase_table.setRowCount(len(purchases))
        for row_index, row_data in enumerate(purchases):
            for col_index, col_data in enumerate(row_data):
                self.purchase_table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def add_supplier(self):
        """Add a new supplier to the database."""
        name = self.supplier_name_input.text().strip()
        contact = self.supplier_contact_input.text().strip()
        address = self.supplier_address_input.text().strip()

        if not name or not contact or not address:
            QMessageBox.warning(self, "Input Error", "All supplier fields are required!")
            return

        try:
            self.cursor.execute("INSERT INTO suppliers (name, contact, address) VALUES (?, ?, ?)", (name, contact, address))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Supplier added successfully!")
            self.load_suppliers()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Supplier with this address already exists.")

    def add_purchase(self):
        """Add a new purchase to the database."""
        supplier_id = self.supplier_combo.currentData()
        category = self.category_combo.currentText()
        quantity = self.product_quantity_input.text().strip()
        unit_price = self.unit_price_input.text().strip()
        purchase_date = self.purchase_date_input.date().toString("yyyy-MM-dd")

        if not supplier_id or not category or not quantity or not unit_price:
            QMessageBox.warning(self, "Input Error", "All purchase fields are required!")
            return

        try:
            quantity = float(quantity)
            unit_price = float(unit_price)
            total_price = quantity * unit_price
            self.cursor.execute(
                """
                INSERT INTO Purchase (supplier_id, product_category, quantity, unit_price, total_price, purchase)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (supplier_id, category, quantity, unit_price, total_price, purchase_date)
            )
            self.conn.commit()
            QMessageBox.information(self, "Success", "Purchase added successfully!")
            self.load_purchases()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add purchase: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PurchaseManagementSystem()
    window.show()
    sys.exit(app.exec_())
