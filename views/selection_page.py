# views/second_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF

class SelectionPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black;")

        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)


        # Create a "mini background" on top with rounded corners
        self.mini_background = QLabel(self)
        self.mini_background.setStyleSheet("""
            background-color: #141414;
            border-radius: 20px;
            margin: 10px;
        """)
        self.mini_background.setAlignment(Qt.AlignCenter)

        # Set layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.mini_background)

        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize mini background to fit inside the parent widget
        self.mini_background.setGeometry(10, 10, self.width() - 20, self.height() - 20)

