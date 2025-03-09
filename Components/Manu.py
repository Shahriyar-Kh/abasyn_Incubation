import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream

# Connect to the database
conn = sqlite3.connect('restaurant_management.db')
cursor = conn.cursor()

class MenuPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Page")
        self.setGeometry(100, 100, 800, 600)

        # Load QSS file
        self.load_stylesheet('Components/styles/menu.qss')

        # Layout for the main menu page
        main_layout = QtWidgets.QVBoxLayout(self)

        # Create a scroll area to handle overflow content
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area_content = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_area_content)
        scroll_area_layout = QtWidgets.QVBoxLayout(scroll_area_content)
        
        # Set ID for the scroll bars
        scroll_area.setObjectName("scrollArea")
        scroll_area.verticalScrollBar().setObjectName("verticalScrollBar")
        scroll_area.horizontalScrollBar().setObjectName("horizontalScrollBar")

        # Add tooltip to the scroll bar
        scroll_area.verticalScrollBar().setToolTip("Scroll to view more items")
        scroll_area.horizontalScrollBar().setToolTip("Scroll horizontally to view more items")

        # Add search frame at the top
        search_frame = self.create_search_frame()
        search_frame.setObjectName("searchFrame")
        main_layout.addWidget(search_frame)

        # Fetch all categories from the database
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = cursor.fetchall()

        # Create a frame for each category and display products
        for category_tuple in categories:
            category = category_tuple[0]  # Extract category name
            products = self.get_products_by_category(category)  # Fetch products for the category
            category_frame = self.create_category_frame(category, products)
            scroll_area_layout.addWidget(category_frame)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def load_stylesheet(self, filename):
        """Load the external QSS file and apply it."""
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        qss = stream.readAll()
        self.setStyleSheet(qss)

    def create_search_frame(self):
        """Create the search bar at the top."""
        search_frame = QtWidgets.QFrame(self)
        search_frame.setObjectName("searchFrame")  # Set ID for the search frame
        search_frame.setStyleSheet("background-color: #ffffff; border-radius: 8px; padding: 20px; margin-bottom: 20px;")
        
        # Search input
        self.search_input = QtWidgets.QLineEdit(search_frame)
        self.search_input.setObjectName("searchInput")  # Set ID for search input
        self.search_input.setPlaceholderText("Search products by name...")
        self.search_input.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid #ccc; font-size: 14px;")
        
        # Search button
        search_button = QtWidgets.QPushButton("Search", search_frame)
        search_button.setObjectName("searchButton")  # Set ID for search button
        search_button.clicked.connect(self.on_search_button_clicked)
        search_button.setStyleSheet("""
        QPushButton {
            background-color: rgb(76, 89, 175);
            color: black;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            font-size: 14px;
            cursor: pointer;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """)

        # Layout for search frame
        search_layout = QtWidgets.QVBoxLayout(search_frame)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        return search_frame

    def on_search_button_clicked(self):
        """Handle search functionality."""
        search_term = self.search_input.text().strip().lower()
        if search_term:
            self.display_products(search_term)
        else:
            self.refresh_page()

    def get_products_by_category(self, category):
        """Fetch products from the database for the given category."""
        cursor.execute("SELECT product_id, name, price, quantity FROM products WHERE category = ?", (category,))
        return cursor.fetchall()

    def display_products(self, search_term):
        """Display products that match the search term."""
        # Clear the existing category frames
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add search frame back at the top
        search_frame = self.create_search_frame()
        self.layout().addWidget(search_frame)

        # Fetch all categories from the database
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = cursor.fetchall()

        # Create a frame for each category and display matching products
        for category_tuple in categories:
            category = category_tuple[0]  # Extract category name
            products = self.get_products_by_category(category)  # Fetch products for the category
            filtered_products = [product for product in products if search_term in product[1].lower()]
            if filtered_products:  # Only create frames if there are products to display
                category_frame = self.create_category_frame(category, filtered_products)
                self.layout().addWidget(category_frame)

    def refresh_page(self):
        """Reload the entire page to show all products."""
        # Clear existing layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add the search frame back at the top
        search_frame = self.create_search_frame()
        self.layout().addWidget(search_frame)

        # Add scroll area to handle overflow content
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area_content = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_area_content)
        scroll_area_layout = QtWidgets.QVBoxLayout(scroll_area_content)

        # Fetch all categories from the database
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = cursor.fetchall()

        # Create a frame for each category and display products
        for category_tuple in categories:
            category = category_tuple[0]  # Extract category name
            products = self.get_products_by_category(category)  # Fetch products for the category
            category_frame = self.create_category_frame(category, products)
            scroll_area_layout.addWidget(category_frame)

        # Add the scroll area to the main layout
        self.layout().addWidget(scroll_area)


    def create_category_frame(self, category, products):
        """Create a dynamic frame for each product category."""
        category_frame = QtWidgets.QFrame(self)
        category_frame.setObjectName(f"categoryFrame_{category}")  # Set ID for category frame
        category_frame.setStyleSheet("background-color: #ffffff; border-radius: 8px; padding: 20px; margin-bottom: 20px;")
        
        # Category title
        category_label = QtWidgets.QLabel(f"<b>{category}</b>", category_frame)
        category_label.setObjectName(f"categoryLabel_{category}")  # Set ID for category label
        category_label.setStyleSheet("font-size: 18px; color: #007bff; padding-bottom: 10px;")

        # Layout for category frame to add the title and product grid
        category_layout = QtWidgets.QVBoxLayout(category_frame)
        category_layout.addWidget(category_label)

        # Create table-like layout (4 columns) for product details
        grid_layout = QtWidgets.QGridLayout()
        
        # Add column headers
        grid_layout.addWidget(QtWidgets.QLabel("Sno"), 0, 0)
        grid_layout.addWidget(QtWidgets.QLabel("Product Name"), 0, 1)
        grid_layout.addWidget(QtWidgets.QLabel("Half Price"), 0, 2)
        grid_layout.addWidget(QtWidgets.QLabel("Full Price"), 0, 3)
        grid_layout.setObjectName('grid_layout')

        # Populate with product details
        row = 1
        for product in products:
            product_id, product_name, product_price, product_qty = product[0], product[1], product[2], product[3]
            half_price = product_price / 2
            full_price = product_price
            grid_layout.addWidget(QtWidgets.QLabel(str(row)), row, 0)
            grid_layout.addWidget(QtWidgets.QLabel(product_name), row, 1)
            grid_layout.addWidget(QtWidgets.QLabel(f"${half_price:.2f}"), row, 2)
            grid_layout.addWidget(QtWidgets.QLabel(f"${full_price:.2f}"), row, 3)
            row += 1
        
        # Add the grid layout to the category frame's layout
        category_layout.addLayout(grid_layout)
        
        category_frame.setLayout(category_layout)
        return category_frame

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MenuPage()
    window.show()
    sys.exit(app.exec_())
