import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QWidget, QMessageBox, QFrame
)
import sqlite3

class CategoryPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Category Management")
        self.setGeometry(200, 200, 800, 400)

        # Initialize the database
        self.conn = sqlite3.connect("restaurant_management.db")
        self.cursor = self.conn.cursor()
        self.init_db()

        self.initUI()
        self.load_data()

        # Apply QSS Styles
        self.load_styles()

    def init_db(self):
        """Create category table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def initUI(self):
        # Main Layout
        main_layout = QHBoxLayout()

        # Frame 1: Input Fields and Buttons
        frame1 = QFrame()
        frame1.setObjectName("frame_input")  # Assign ID for QSS
        frame1_layout = QVBoxLayout()

        # Category Name Label and Field
        category_label = QLabel("Category Name:")
        category_label.setObjectName("category_label")  # Assign ID for QSS
        self.name_input = QLineEdit()
        self.name_input.setObjectName("name_input")  # Assign ID for QSS
        self.name_input.setPlaceholderText("Enter category name")
        frame1_layout.addWidget(category_label)
        frame1_layout.addWidget(self.name_input)

        # Buttons in rows
        button_row1 = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.add_button.setObjectName("add_button")  # Assign ID for QSS
        self.update_button = QPushButton("Update")
        self.update_button.setObjectName("update_button")  # Assign ID for QSS
        button_row1.addWidget(self.add_button)
        button_row1.addWidget(self.update_button)

        button_row2 = QHBoxLayout()
        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("delete_button")  # Assign ID for QSS
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("clear_button")  # Assign ID for QSS
        button_row2.addWidget(self.delete_button)
        button_row2.addWidget(self.clear_button)

        frame1_layout.addLayout(button_row1)
        frame1_layout.addLayout(button_row2)
        frame1.setLayout(frame1_layout)

        # Frame 2: Data Table and Search Filter
        frame2 = QFrame()
        frame2.setObjectName("frame_table")  # Assign ID for QSS
        frame2_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")  # Assign ID for QSS
        self.search_input.setPlaceholderText("Search categories")
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("search_button")  # Assign ID for QSS
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        self.table = QTableWidget()
        self.table.setObjectName("category_table")  # Assign ID for QSS
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Category Name"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)

        frame2_layout.addLayout(search_layout)
        frame2_layout.addWidget(self.table)
        frame2.setLayout(frame2_layout)

        # Add frames to main layout
        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)

        # Set central widget
        container = QWidget()
        container.setObjectName("main_container")  # Assign ID for QSS
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect signals
        self.add_button.clicked.connect(self.add_category)
        self.update_button.clicked.connect(self.update_category)
        self.delete_button.clicked.connect(self.delete_category)
        self.clear_button.clicked.connect(self.clear_input)
        self.search_button.clicked.connect(self.search_category)
        self.table.itemSelectionChanged.connect(self.populate_input_from_table)

    def load_styles(self):
        """Load QSS file to apply styles."""
        with open("Components/styles/cat.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_data(self):
        """Load all category data into the table."""
        self.cursor.execute("SELECT * FROM category")
        rows = self.cursor.fetchall()
        self.display_table(rows)

    def display_table(self, rows):
        """Display given rows in the table."""
        self.table.setRowCount(0)
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(row[1]))

    def add_category(self):
        """Add a new category to the database with validation."""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Category name cannot be empty.")
            return

        # Check if the category already exists
        self.cursor.execute("SELECT COUNT(*) FROM category WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        if result[0] > 0:
            QMessageBox.warning(self, "Duplicate Category", "This category already exists.")
            return

        # If it doesn't exist, add the new category
        self.cursor.execute("INSERT INTO category (name) VALUES (?)", (name,))
        self.conn.commit()
        
        self.load_data()
        QMessageBox.information(self, "Success", "Category added successfully.")
        self.clear_input()
      


    def update_category(self):
        """Update the selected category in the database."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a category to update.")
            return

        category_id = self.table.item(selected_row, 0).text()
        new_name = self.name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Input Error", "Category name cannot be empty.")
            return

        self.cursor.execute("UPDATE category SET name = ? WHERE id = ?", (new_name, category_id))
        self.conn.commit()
       
        self.load_data()
        QMessageBox.information(self, "Success", "Category updated successfully.")
        self.clear_input()

    def delete_category(self):
        """Delete the selected category from the database."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a category to delete.")
            return

        category_id = self.table.item(selected_row, 0).text()
        self.cursor.execute("DELETE FROM category WHERE id = ?", (category_id,))
        self.conn.commit()
        self.load_data()
        QMessageBox.information(self, "Success", "Category deleted successfully.")
        self.clear_input()

    def search_category(self):
        """Filter the table based on the search input."""
        search_term = self.search_input.text().strip()
        if search_term:
            self.cursor.execute("SELECT * FROM category WHERE name LIKE ?", ('%' + search_term + '%',))
        else:
            self.cursor.execute("SELECT * FROM category")
        rows = self.cursor.fetchall()
        self.display_table(rows)

    def clear_input(self):
        """Clear the input fields."""
        self.name_input.clear()
        self.table.clearSelection()

    def populate_input_from_table(self):
        """Populate the input field with data from the selected row."""
        selected_row = self.table.currentRow()
        if selected_row != -1:
            self.name_input.setText(self.table.item(selected_row, 1).text())

    def closeEvent(self, event):
        """Ensure the database connection is closed on exit."""
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CategoryPage()
    window.show()
    sys.exit(app.exec_())
