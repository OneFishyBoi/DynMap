# main.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QIcon
from views.landing_page import LandingPage
from views.selection_page import SelectionPage
from views.mapping_page import MappingPage
import os

class AppController(QMainWindow):
    # initialising the app controller
    # This class manages the navigation between different pages in the application.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DynMap")

        # setting the icon for the application window
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "icon.png")
        self.setWindowIcon(QIcon(icon_path))

        # a custom pyqt5 stack of pages that allows for fast swapping between different pages
        # without having to create new instances of the pages each time
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Shared data (optional)
        self.shared_data = {}

        # Instantiate pages with app controller reference
        # This allows each page to call methods in the controller for navigation and data sharing.
        self.landing_page = LandingPage(self)
        self.selection_page = SelectionPage(self)
        self.mapping_page = MappingPage(self)

        # Add pages to stack
        self.stack.addWidget(self.landing_page)
        self.stack.addWidget(self.selection_page)
        self.stack.addWidget(self.mapping_page)

        # Show landing page initially
        self.stack.setCurrentWidget(self.selection_page)

    def switch_to_selection(self):
        self.stack.setCurrentWidget(self.selection_page)

    def switch_to_landing(self):
        self.stack.setCurrentWidget(self.landing_page)

    def switch_to_mapping(self):
        self.stack.setCurrentWidget(self.mapping_page)


if __name__ == "__main__":
    app = QApplication([])
    window = AppController()

    # Get screen geometry
    screen = QDesktopWidget().screenGeometry()
    width, height = screen.width(), screen.height()

    # Set the window size to match screen size
    window.setGeometry(0, 0, width, height)

    window.showMaximized()
    app.exec_()
