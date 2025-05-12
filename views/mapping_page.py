# views/landing_page.py
from PyQt5.QtWidgets import QWidget

# creating the landing page class that inherits from QWidget (a base class for all UI objects in PyQt5)
# This class represents the initial page of the application.
class MappingPage(QWidget):
    def __init__(self, controller):
        # Initialising the landing page class with a reference to the controller
        # This allows the landing page to call methods in the controller for navigation and data sharing.
        super().__init__()
        self.controller = controller
