# views/second_page.py
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class SelectionPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black;")

        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Replace QLabel with QWidget for layout capability
        self.mini_background = QWidget(self)
        self.mini_background.setStyleSheet("""
            background-color: #141414;
            border-radius: 20px;
            margin: 10px;
        """)

        # Set grid layout inside mini_background
        grid_layout = QGridLayout(self.mini_background)

        # button to add new maps
        add_button = QPushButton("+")
        add_button.clicked.connect(self.addButtonClicked)
        grid_layout.addWidget(add_button, 0, 0)

        # styling button
        add_button.setStyleSheet("""
        QPushButton {
            border: 2px solid white;       /* Outline */
            border-radius: 6px;
            font-size: 50px;               /* Text size */
            color: white;                  /* Text color */
            background-color: #444;        /* Optional background */
            height: 300px;                /* Button height */
        }
        QPushButton:hover {
            border-color: cyan;            /* Outline color on hover */
        }
        """)
                
        # adding empty pagging for grid display
        grid_layout.addWidget(QLabel(""), 0, 1)
        grid_layout.addWidget(QLabel(""), 0, 2)
        grid_layout.addWidget(QLabel(""), 1, 0)
        grid_layout.addWidget(QLabel(""), 2, 0)

        # adding delete button and open button
        bottom_button = QPushButton("BIN")
        open_button = QPushButton("OPEN")

        # styling both buttons
        for button in (bottom_button, open_button):
            button.setFixedSize(80, 60)
            button.setStyleSheet("""
                QPushButton {
                    border: 2px solid white;
                    border-radius: 5px;
                    font-size: 20px;
                    color: white;
                    background-color: #333;
                    font-weight: bold;
                }
                QPushButton:hover {
                    border-color: cyan;
                }
            """)

        # bottom row layout with left and right sections
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(20, 20, 20, 20)

        # Left side: OPEN button
        left_box = QHBoxLayout()
        left_box.addWidget(open_button)
        left_box.addStretch()

        # Right side: BIN button
        right_box = QHBoxLayout()
        right_box.addStretch()
        right_box.addWidget(bottom_button)

        # Add left and right to bottom row
        bottom_row.addLayout(left_box)
        bottom_row.addStretch()
        bottom_row.addLayout(right_box)

        # Wrap in vertical layout to push it to bottom
        bottom_layout = QVBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addLayout(bottom_row)

        # Set main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.mini_background)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize mini background to fit inside the parent widget
        self.mini_background.setGeometry(10, 10, self.width() - 20, self.height() - 20)

    def addButtonClicked(self):
        # Move the add button to new position
        # Add the new map to the grid layout
        



