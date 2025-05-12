# views/landing_page.py
from PyQt5.QtWidgets import QWidget, QLabel, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
import time

# creating the landing page class that inherits from QWidget (a base class for all UI objects in PyQt5)
# This class represents the initial page of the application.
class LandingPage(QWidget):
    def __init__(self, controller):
        # Initialising the landing page class with a reference to the controller
        # This allows the landing page to call methods in the controller for navigation and data sharing.
        super().__init__()
        self.controller = controller

        self.setStyleSheet("background-color: #121212;") 

        # Create background image as QLabel
        self.bg_label = QLabel(self)
        pixmap = QPixmap("C:/Users/finla/Documents/Projects/DynMap/DynMap/resources/landing_page_background.png")
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.resize(self.size())
        self.bg_label.lower()
        
        # settings keyboard focus for event handling
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event):
        self.zoom_in_background()
        self.fade_to_black()

    def resizeEvent(self, event):
        # Resize background image with window
        self.bg_label.resize(self.size())

    def zoom_in_background(self):
        # Get current geometry of the label
        current_rect = self.bg_label.geometry()
        
        # Define target geometry (e.g., 20% larger and centered)
        scale_factor = 10
        new_width = int(current_rect.width() * scale_factor)
        new_height = int(current_rect.height() * scale_factor)
        new_x = int(current_rect.x() - (new_width - current_rect.width()) / 2)
        new_y = int(current_rect.y() - (new_height - current_rect.height()) / 2)

        # Animate geometry change
        self.anim = QPropertyAnimation(self.bg_label, b"geometry")
        self.anim.setDuration(5000)  # in ms
        self.anim.setStartValue(current_rect)
        self.anim.setEndValue(QRect(new_x, new_y, new_width, new_height))
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()

    def fade_to_black(self):
        # Apply the opacity effect to the QLabel that holds the pixmap
        self.opacity_effect = QGraphicsOpacityEffect(self.bg_label)
        self.bg_label.setGraphicsEffect(self.opacity_effect)

        # Store the animation on self to prevent garbage collection
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(1000)  # Fade over 1 second
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Optional: trigger page switch after fade
        self.opacity_anim.finished.connect(self.controller.switch_to_selection)

        # Start the fade animation
        self.opacity_anim.start()

        
