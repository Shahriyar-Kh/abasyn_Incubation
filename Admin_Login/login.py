import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Dashboard')))
from dashboard import DashboardClass  # Import your existing dashboard script

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 400, 300)
        self.setFixedSize(600, 500)  # Prevent resizing for better design
        self.init_ui()

        # Load external stylesheet
        self.load_stylesheet()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Login to Restaurant System")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Username Field
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Enter Username")
        layout.addWidget(self.username_field)

        # Password Field
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_field)

        # Login Button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.authenticate)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def load_stylesheet(self):
        """Load external CSS stylesheet."""
        stylesheet_path = os.path.join(os.path.dirname(__file__), "login.qss")
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as file:
                self.setStyleSheet(file.read())
        else:
            QMessageBox.warning(self, "Error", "Stylesheet not found!")

    def authenticate(self):
        """Handle Login Logic"""
        username = self.username_field.text()
        password = self.password_field.text()

        # Hardcoded credentials for demo purposes
        if username == "shary" and password == "shary786":
            self.open_dashboard()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")

    def open_dashboard(self):
        """Open Dashboard on Successful Login"""
        username = self.username_field.text()  # Get the username
        self.close()  # Close the login window
        self.dashboard = DashboardClass(username)  # Pass the username to DashboardClass
        self.dashboard.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginPage()
    login.show()
    sys.exit(app.exec_())

