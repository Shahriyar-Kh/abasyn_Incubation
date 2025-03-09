import sqlite3
import os
import shutil

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, 
    QTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QGroupBox, QHeaderView, QMessageBox, QFileDialog, QDateEdit
)
from PyQt5.QtCore import Qt, QDate


DB_NAME = "restaurant_management.db"

class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Management System - Employee Management")
        self.setGeometry(100, 100, 1400, 800)
        
        self.apply_stylesheet()  # Load QSS Stylesheet
        self.init_ui()
        self.load_employees()
        # Define the path for storing employee images
        self.employee_images_path = 'Employee_images'
        if not os.path.exists(self.employee_images_path):
            os.makedirs(self.employee_images_path)
        self.setObjectName("employee-management-page")


    def apply_stylesheet(self):
        """Load QSS Stylesheet."""
        try:
            with open("Components/styles/employee_style.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Stylesheet file 'employee_page.qss' not found!")

    def init_ui(self):
        # Main Layout
        main_layout = QVBoxLayout(self)

        # Search Section
        search_group = QGroupBox("Search Employee")
        search_layout = QHBoxLayout()

        self.search_type = QComboBox()
        self.search_type.addItems(["Select by", "Employee ID", "Name", "Email", "Phone"])
        self.search_input = QLineEdit()
        search_button = QPushButton("Search")
        search_button.setObjectName("Search-button")
        search_button.clicked.connect(self.search_employee)

        search_layout.addWidget(self.search_type)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_group.setLayout(search_layout)
        search_group.setObjectName("search-section")
        main_layout.addWidget(search_group)

     # Employee Details Form
        details_group = QGroupBox("Employee Details")
        form_layout = QFormLayout()
        details_group.setObjectName("employee-details-form")

        # Left Column
        left_layout = QVBoxLayout()
        self.emp_id = QLineEdit()
        
        self.emp_id.setReadOnly(True)
        self.name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()

        left_layout.addWidget(QLabel("Employee ID:"))
        left_layout.addWidget(self.emp_id)
        left_layout.addWidget(QLabel("Name:"))
        left_layout.addWidget(self.name)
        left_layout.addWidget(QLabel("Email:"))
        left_layout.addWidget(self.email)
        left_layout.addWidget(QLabel("Phone:"))
        left_layout.addWidget(self.phone)

        # Middle Column
        middle_layout = QVBoxLayout()
        self.id_card = QLineEdit()
        self.address = QLineEdit()
        self.position = QComboBox()
        self.position.addItems(["Select Position", "chef", "waiter", "manager", "cleaner"])
        self.salary = QLineEdit()

        middle_layout.addWidget(QLabel("ID Card Number:"))
        middle_layout.addWidget(self.id_card)
        middle_layout.addWidget(QLabel("Address:"))
        middle_layout.addWidget(self.address)
        middle_layout.addWidget(QLabel("Position:"))
        middle_layout.addWidget(self.position)
        middle_layout.addWidget(QLabel("Salary:"))
        middle_layout.addWidget(self.salary)

        # Right Column
        right_layout = QVBoxLayout()
        self.hire_date = QDateEdit()
        self.hire_date.setCalendarPopup(True)
        self.hire_date.setDate(QDate.currentDate())
        self.status = QComboBox()
        self.status.addItems(["active", "inactive"])
        self.profile_picture_path = QLineEdit()
        self.profile_picture_path.setReadOnly(True)
        browse_button = QPushButton("Uplaod")
        browse_button.setObjectName("Uplaod-button")
        browse_button.clicked.connect(self.browse_picture)

        right_layout.addWidget(QLabel("Hire Date:"))
        right_layout.addWidget(self.hire_date)
        right_layout.addWidget(QLabel("Status:"))
        right_layout.addWidget(self.status)
        right_layout.addWidget(QLabel("Profile Picture:"))
        right_layout.addWidget(self.profile_picture_path)
        right_layout.addWidget(browse_button)

        # Combine Columns
        form_column_layout = QHBoxLayout()
        form_column_layout.addLayout(left_layout)
        form_column_layout.addLayout(middle_layout)
        form_column_layout.addLayout(right_layout)

        details_group.setLayout(form_column_layout)
        main_layout.addWidget(details_group)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_employee)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_employee)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_employee)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_fields)
        #++++++++++++++++++ buttons ids ===============
        save_button.setObjectName("save-button")
        update_button.setObjectName("update-button")
        delete_button.setObjectName("delete-button")
        clear_button.setObjectName("clear-button")
        

        button_layout.addWidget(save_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)
        main_layout.addLayout(button_layout)


        # Employee Table
        self.employee_table = QTableWidget()
        self.employee_table.setObjectName("employee-table")
        self.employee_table.setColumnCount(11)
        self.employee_table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Email", "Phone", "Address", 
            "Position", "Salary", "Hire Date", "Status","NIC","Profile Picture"
        ])
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employee_table.cellClicked.connect(self.load_employee_details)
        main_layout.addWidget(self.employee_table)

    # Browse Profile Picture
    def browse_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.profile_picture_path.setText(file_path)

    # Database Operations
    def connect_db(self):
        return sqlite3.connect(DB_NAME)

    def load_employees(self):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        connection.close()

        self.employee_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.employee_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def save_employee(self):
        # Connect to the database
        connection = self.connect_db()
        cursor = connection.cursor()
        try:
            # Fetch the next available ID (if using AUTOINCREMENT, fetch the last inserted ID)
            cursor.execute("SELECT MAX(id) FROM employees")
            result = cursor.fetchone()
            if result and result[0] is not None:
                next_id = result[0] + 1  # Increment the max ID by 1
            else:
                next_id = 1  # Start at 1 if no records exist

            # Update the emp_id field with the next ID
            self.emp_id.setText(str(next_id))

            # Get the profile picture file path
            picture_path = self.profile_picture_path.text()
            new_picture_path = None
            if picture_path:
                # Create a new file name for the image and move it to the 'Employee_images' folder
                employee_name = self.name.text().replace(" ", "_")  # Use a sanitized name for the file
                new_picture_path = os.path.join(self.employee_images_path, f"{employee_name}_profile.jpg")
                try:
                    shutil.copy(picture_path, new_picture_path)  # Copy the selected image to the folder
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save the profile picture: {e}")
                    return

            # Save employee details, including the new picture path, to the database
            cursor.execute(
                "INSERT INTO employees (id, name, email, phone, address, position, salary, hire_date, status, id_card, profile_picture) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    next_id,  # Use the calculated ID
                    self.name.text(),
                    self.email.text(),
                    self.phone.text(),
                    self.address.text(),
                    self.position.currentText(),
                    float(self.salary.text()) if self.salary.text() else 0.0,
                    self.hire_date.text(),
                    self.status.currentText(),
                    self.id_card.text(),
                    new_picture_path,  # Save the path to the image in the database
                )
            )
            connection.commit()
            QMessageBox.information(self, "Success", "Employee added successfully!")
            self.load_employees()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add employee: {e}")
        finally:
            connection.close()



    def update_employee(self):
        # Get the updated profile picture file path
        picture_path = self.profile_picture_path.text()
        new_picture_path = None  # Initialize variable for new path

        if picture_path:
            # Create a new file name for the image and move it to the 'Employee_images' folder
            employee_name = self.name.text().replace(" ", "_")  # Use a sanitized name for the file
            new_picture_path = os.path.join(self.employee_images_path, f"{employee_name}_profile.jpg")

            # Check if the source and destination are the same
            if os.path.abspath(picture_path) != os.path.abspath(new_picture_path):
                try:
                    shutil.copy(picture_path, new_picture_path)  # Copy the selected image to the folder
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save the profile picture: {e}")
                    return
        else:
            # If no new picture is selected, keep the old picture path
            new_picture_path = self.profile_picture_path.text()

        # Reset styles for all fields
        self.reset_field_styles()

        # Validate required fields
        missing_fields = []
        if not self.name.text():
            missing_fields.append(self.name)
        if not self.email.text():
            missing_fields.append(self.email)
        if not self.phone.text():
            missing_fields.append(self.phone)
        if not self.id_card.text():
            missing_fields.append(self.id_card)
        if not self.address.text():
            missing_fields.append(self.address)
        if self.position.currentText() == "Select Position":
            missing_fields.append(self.position)
        if not self.salary.text():
            missing_fields.append(self.salary)
        if not self.hire_date.text():
            missing_fields.append(self.hire_date)

        # Highlight missing fields in red
        if missing_fields:
            for field in missing_fields:
                field.setStyleSheet("border: 2px solid red;")
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields!")
            return

        # Update employee details, including the new picture path, in the database
        connection = self.connect_db()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE employees SET name = ?, email = ?, phone = ?, address = ?, position = ?, "
                "salary = ?, hire_date = ?, status = ?, id_card = ?, profile_picture = ? WHERE employee_id = ?",
                (
                    self.name.text(),
                    self.email.text(),
                    self.phone.text(),
                    self.address.text(),
                    self.position.currentText(),
                    float(self.salary.text()),
                    self.hire_date.text(),
                    self.status.currentText(),
                    self.id_card.text(),
                    new_picture_path,  # Save the updated path to the image in the database
                    int(self.emp_id.text()),
                )
            )
            connection.commit()
            QMessageBox.information(self, "Success", "Employee updated successfully!")
            self.load_employees()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update employee: {e}")
        finally:
            connection.close()

    def reset_field_styles(self):
        """Reset the border style of all fields to default."""
        fields = [
            self.name, self.email, self.phone, self.id_card,self.address, self.salary, self.hire_date, self.position,self.profile_picture_path
        ]
        for field in fields:
            field.setStyleSheet("")

    def delete_employee(self):
        connection = self.connect_db()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM employees WHERE employee_id = ?", (int(self.emp_id.text()),))
            connection.commit()
            QMessageBox.information(self, "Success", "Employee deleted successfully!")
            self.load_employees()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete employee: {e}")
        finally:
            connection.close()


    def search_employee(self):
        search_by = self.search_type.currentText()
        search_text = self.search_input.text()
        if search_by == "Select by" or not search_text:
            QMessageBox.warning(self, "Warning", "Please select a search type and enter a value.")
            return

        query_map = {
            "Employee ID": "employee_id",
            "Name": "name",
            "Email": "email",
            "Phone": "phone",
        }

        column = query_map.get(search_by, None)
        if not column:
            QMessageBox.critical(self, "Error", "Invalid search type selected.")
            return

        connection = self.connect_db()
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM employees WHERE {column} LIKE ?", (f"%{search_text}%",))
            rows = cursor.fetchall()
            self.employee_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.employee_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed: {e}")
        finally:
            connection.close()


    def load_employee_details(self, row):
        self.emp_id.setText(self.employee_table.item(row, 0).text())
        self.name.setText(self.employee_table.item(row, 1).text())
        self.email.setText(self.employee_table.item(row, 2).text())
        self.phone.setText(self.employee_table.item(row, 3).text())
        self.address.setText(self.employee_table.item(row, 4).text())
        self.position.setCurrentText(self.employee_table.item(row, 5).text())
        self.salary.setText(self.employee_table.item(row, 6).text())
       # Convert string to QDate for hire_date
        hire_date_str = self.employee_table.item(row, 7).text()  # Example: "2023-01-07"
        hire_date = QDate.fromString(hire_date_str, "yyyy-MM-dd")  # Adjust format to match your data
        self.hire_date.setDate(hire_date)
        self.status.setCurrentText(self.employee_table.item(row, 8).text())
        self.id_card.setText(self.employee_table.item(row, 9).text())
            # Check if profile picture path column exists
        profile_picture_item = self.employee_table.item(row, 10)
        if profile_picture_item is not None:
            self.profile_picture_path.setText(profile_picture_item.text())
        else:
            self.profile_picture_path.setText("")  # Clear if no picture path is available

    def clear_fields(self):
            self.emp_id.clear()
            self.name.clear()
            self.email.clear()
            self.phone.clear()
            self.address.clear()
            self.position.setCurrentIndex(0)
            self.salary.clear()
            self.hire_date.clear()
            self.status.setCurrentIndex(0)
            self.id_card.clear()
            self.profile_picture_path.clear()
            



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = EmployeePage()
    window.show()
    sys.exit(app.exec_())
