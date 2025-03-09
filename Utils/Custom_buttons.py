from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class WindowControls(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # Layout for the custom window controls
        self.layout = QHBoxLayout(self)

        # Create minimize, maximize, and close buttons
        self.minimize_button = QPushButton("_", self)
        self.maximize_button = QPushButton("□", self)
        self.close_button = QPushButton("X", self)
                # Set professional colors for buttons
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #B0B0B0;  /* Neutral gray */
                border: none;
                font-size: 16px;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8E8E8E;  /* Darker gray on hover */
            }
        """)

        self.maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Soft green */
                border: none;
                font-size: 16px;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;  /* Slightly darker green on hover */
            }
        """)

        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;  /* Soft red */
                border: none;
                font-size: 16px;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;  /* Darker red on hover */
            }
        """)

        # Connect buttons to their respective functions
        self.minimize_button.clicked.connect(parent.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(parent.close)

        # Add a spacer to push the buttons to the right
        self.layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Add buttons to the layout
        self.layout.addWidget(self.minimize_button)
        self.layout.addWidget(self.maximize_button)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def toggle_maximize(self):
        """Toggle between maximizing and restoring the window."""
        parent = self.parent()
        if parent.isMaximized():
            parent.showNormal()
        else:
            parent.showMaximized()
