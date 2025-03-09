import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QDialog,
    QLabel, QPushButton, QWidget, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt5.QtGui import QPainter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.Custom_buttons import WindowControls
# Adjust sys.path to include the Components folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Components')))
from Employees import EmployeePage  # Now we can import from Components
from Product_M import ProductManagementUI
from Manu import MenuPage
from order_m import OrderManagementPage
from stock_m import StockManagementPage


class DashboardClass(QMainWindow):
    def __init__(self,username='Admin'):
        super().__init__()
        self.username = username  # Store the username
        self.setWindowTitle("Restaurant Management System")
        self.setGeometry(100, 100, 1200, 800)

        # Load the external CSS file
        self.load_styles()

        # Main Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QVBoxLayout(self.central_widget)

        # Top Section
        top_section = self.create_top_section()
        main_layout.addWidget(top_section)

        # Middle Section (Sidebar + Main Area)
        middle_section = QHBoxLayout()
        sidebar = self.create_sidebar()
        main_area = self.create_main_area()
        middle_section.addWidget(sidebar)
        middle_section.addWidget(main_area)
        main_layout.addLayout(middle_section)

        # Bottom Section
        bottom_section = self.create_bottom_section()
        main_layout.addWidget(bottom_section)

    def load_styles(self):
        """Load the styles.qss file."""
        with open("Dashboard/dashboard.qss", "r") as style_file:
            self.setStyleSheet(style_file.read())

    def create_top_section(self):
        """Create the top section with restaurant name and user authentication."""
        top_frame = QFrame()
        top_frame.setObjectName("topFrame")
        top_frame.setFixedHeight(80)
        top_layout = QHBoxLayout(top_frame)

        # Restaurant Name
        rest_name_label = QLabel("Restaurant Management System")
        top_layout.addWidget(rest_name_label, alignment=Qt.AlignLeft)

        # User Authentication
        auth_label = QLabel(f"Logged in as: {self.username}")
        top_layout.addWidget(auth_label, alignment=Qt.AlignRight)

        return top_frame


    def create_main_area(self):
        """Create the main area for displaying content."""
        main_area_frame = QFrame()
        main_area_frame.setObjectName("mainAreaFrame")
        main_area_layout = QGridLayout(main_area_frame)

        # First Row: Unpaid Orders and Shortage Products
        unpaid_orders_label = QLabel("Unpaid Orders ")
        self.unpaid_orders_count = QLabel("0")  # Placeholder value
        shortage_products_label = QLabel("Shortage Products ")
        self.shortage_products_count = QLabel("0")  # Placeholder value

        main_area_layout.addWidget(unpaid_orders_label, 0, 0)
        main_area_layout.addWidget(self.unpaid_orders_count, 0, 1)
        main_area_layout.addWidget(shortage_products_label, 0, 2)
        main_area_layout.addWidget(self.shortage_products_count, 0, 3)

        # Second Row: Sales Record Graph
        sales_label = QLabel("Sales Record (Graph):")
        main_area_layout.addWidget(sales_label, 1, 0, 1, 4)  # Spans all columns
        self.sales_chart_view = self.create_sales_chart()
        main_area_layout.addWidget(self.sales_chart_view, 2, 0, 1, 4)  # Spans all columns

        # Load data
        self.update_dashboard_data()

        return main_area_frame




    def create_bottom_section(self):
        """Create the bottom section with project development information."""
        bottom_frame = QFrame()
        bottom_frame.setObjectName("bottomFrame")
        bottom_frame.setFixedHeight(70)
        bottom_layout = QHBoxLayout(bottom_frame)

        # Development Information
        dev_info_label = QLabel("Developed by: Shahriyar Khan")
        bottom_layout.addWidget(dev_info_label, alignment=Qt.AlignCenter)

        return bottom_frame
    
    def create_sidebar(self):
        """Create the sidebar with menu options."""
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebarFrame")
        sidebar_frame.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar_frame)

        # Add buttons for sidebar options with their respective functions
        button1 = QPushButton("Employee Management")
        button1.clicked.connect(self.employee_management)
        sidebar_layout.addWidget(button1)

        button2 = QPushButton("Product Management")
        button2.clicked.connect(self.product_management)
        sidebar_layout.addWidget(button2)

        button3 = QPushButton("Menu")
        button3.clicked.connect(self.menu)
        sidebar_layout.addWidget(button3)

        button4 = QPushButton("Order Management")
        button4.clicked.connect(self.order_management)
        sidebar_layout.addWidget(button4)

        button5 = QPushButton("Product Supply Management")
        button5.clicked.connect(self.product_supply_management)
        sidebar_layout.addWidget(button5)

        button6 = QPushButton("Sales Management")
        button6.clicked.connect(self.sales_management)
        sidebar_layout.addWidget(button6)

        button7 = QPushButton("Stock Management")
        button7.clicked.connect(self.stock_management)
        sidebar_layout.addWidget(button7)

        sidebar_layout.addStretch()
        return sidebar_frame
    
    def update_dashboard_data(self):
        """Update dashboard data."""
        conn = sqlite3.connect("restaurant_management.db")
        cursor = conn.cursor()

        # Unpaid Orders Count
        cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Unpaid'")
        unpaid_count = cursor.fetchone()[0]
        self.unpaid_orders_count.setText(str(unpaid_count))

        # Shortage Products Count
        cursor.execute("SELECT COUNT(*) FROM stock WHERE quantity <= low_stock_threshold")
        shortage_count = cursor.fetchone()[0]
        self.shortage_products_count.setText(str(shortage_count))

        # Sales Data
        cursor.execute("SELECT strftime('%Y-%m-%d', current_datetime) AS sale_date, SUM(total_price) "
                       "FROM orders WHERE status = 'Paid' GROUP BY sale_date")
        sales_data = cursor.fetchall()
        self.update_sales_chart(sales_data)

        conn.close()

    def create_sales_chart(self):
        """Create a bar chart for sales data."""
        chart = QChart()
        chart.setTitle("Sales Record (Daily)")
        series = QBarSeries()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view

    def update_sales_chart(self, sales_data):
        """Update the sales chart with new data."""
        chart = self.sales_chart_view.chart()
        series = QBarSeries()
        categories = []
        for date, total in sales_data:
            bar_set = QBarSet(date)
            bar_set << total
            series.append(bar_set)
            categories.append(date)

        chart.removeAllSeries()
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%i")
        chart.setAxisX(axis_x, series)
        chart.setAxisY(axis_y, series)



    def employee_management(self):
        """Function to open Employee Management in a separate window."""
        # Create a new instance of EmployeePage
        self.employee_page = EmployeePage()  # Keep a reference to avoid garbage collection

        # Set the window flags for normal window behavior (with title bar, minimize/maximize/close)
        self.employee_page.setWindowFlags(Qt.Window)

        # Show the employee page as a standalone window
        self.employee_page.show()



    def product_management(self):
        """Function to open Employee Management in a separate window."""
        # Create a new instance of EmployeePage
        self.product_page = ProductManagementUI()  # Keep a reference to avoid garbage collection

        # Set the window flags for normal window behavior (with title bar, minimize/maximize/close)
        self.product_page.setWindowFlags(Qt.Window)

        # Show the employee page as a standalone window
        self.product_page.show()

    def menu(self):
        """Function to open Employee Management in a separate window."""
        # Create a new instance of EmployeePage
        self.menu_page =MenuPage()  # Keep a reference to avoid garbage collection

        # Set the window flags for normal window behavior (with title bar, minimize/maximize/close)
        self.menu_page.setWindowFlags(Qt.Window)

        # Show the employee page as a standalone window
        self.menu_page.show()

    def order_management(self):
        """Function to open Employee Management in a separate window."""
        # Create a new instance of EmployeePage
        self.order_page =OrderManagementPage()  # Keep a reference to avoid garbage collection
     
        # Set the window flags for normal window behavior (with title bar, minimize/maximize/close)
        self.order_page.setWindowFlags(Qt.Window)

        # Show the employee page as a standalone window
        self.order_page.show()

    def product_supply_management(self):
     pass

    def sales_management(self):
       pass  


    def stock_management(self):
        """Function to open Employee Management in a separate window."""
        # Create a new instance of EmployeePage
        self.stock =StockManagementPage()  # Keep a reference to avoid garbage collection
     
        # Set the window flags for normal window behavior (with title bar, minimize/maximize/close)
        self.stock.setWindowFlags(Qt.Window)

        # Show the employee page as a standalone window
        self.stock.show()
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = DashboardClass()
    dashboard.show()
    sys.exit(app.exec_())
