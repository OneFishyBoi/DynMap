# views/second_page.py
from PyQt5.QtWidgets import QWidget, QLabel

class SelectionPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Set layout so it fills the space
        label = QLabel("This is the selection page", self)
        label.setStyleSheet("color: black; font-size: 20px;")
        label.move(100, 100)

        self.setStyleSheet("background-color: grey; border: 3px solid red;")
