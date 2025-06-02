# views/landing_page.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QIcon
from PyQt5.QtCore import Qt
import os

# creating the landing page class that inherits from QWidget (a base class for all UI objects in PyQt5)
# This class represents the initial page of the application.
class MappingPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # setting the keyboard focus on the page so that it can receive keyboard events
        self.setFocusPolicy(Qt.StrongFocus)

        # Set the background color of the page
        self.setStyleSheet("background-color: #141414;")
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # creating the canvas to draw on
        # Create a QPixmap as the canvas and fill it with a dark background
        self.canvas = QPixmap(self.size())
        self.canvas.fill(QColor("#141414"))

        # Stores the last mouse position
        self.last_point = None

        # stores the history of drawn lines
        self.history = []

        # stores the current pen colour defaulting to white
        self.current_pen_color = QColor("white")

        # stores the current pen size defaulting to small
        self.current_pen_size = 1

        # creating a pen size selector
        small_pen_button = self.create_size_button("1", "Small Pen")
        medium_pen_button = self.create_size_button("3", "Medium Pen")
        large_pen_button = self.create_size_button("5", "Large Pen")
        very_large_pen_button = self.create_size_button("10", "Very Large Pen")
        massize_pen_button = self.create_size_button("30", "Massive Pen")

        self.size_buttons = [
            small_pen_button,
            medium_pen_button,
            large_pen_button,
            very_large_pen_button,
            massize_pen_button
        ]
        for button in self.size_buttons:
            # Connect each button to the change_pen_size method
            button.clicked.connect(lambda _, b=button: self.change_pen_size(b))

        # creating colour pen buttons
        white_pen_button = self.create_color_button("white", "White Pen")
        purple_pen_button = self.create_color_button("purple", "Purple Pen")
        blue_pen_button = self.create_color_button("blue", "Blue Pen")
        golden_pen_button = self.create_color_button("gold", "Golden Pen")
        red_pen_button = self.create_color_button("red", "Red Pen")
        eraser_button = self.create_color_button("white", "Eraser")

        # connecting the buttons to their respective functions
        self.colour_buttons = [
            white_pen_button,
            purple_pen_button,
            blue_pen_button,
            golden_pen_button,
            red_pen_button,
            eraser_button
        ]
        for button in self.colour_buttons:
            # Connect each button to the change_pen_color method
            button.clicked.connect(lambda _, b=button: self.change_pen_color(b))

        # adding the eraser icon
        eraser_button.setIcon(QIcon("C:/Users/finla/Documents/Projects/DynMap/DynMap/resources/eraser.png"))

        # Set the initial pen color to white
        self.selectColorButton(white_pen_button)

        # set the inital pen size to small
        self.change_pen_size(small_pen_button)

        # creating layout for the colour buttons
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        for button in self.colour_buttons:
            horizontal_layout.addWidget(button)

        # creating layout for the pen size buttons
        inner_pen_size_layout = QVBoxLayout()
        inner_pen_size_layout.addWidget(small_pen_button)
        inner_pen_size_layout.addWidget(medium_pen_button)
        inner_pen_size_layout.addWidget(large_pen_button)
        inner_pen_size_layout.addWidget(very_large_pen_button)   
        inner_pen_size_layout.addWidget(massize_pen_button)
        pen_size_layout = QHBoxLayout()
        pen_size_layout.addStretch()
        pen_size_layout.addLayout(inner_pen_size_layout)

        # creating a vertical to place buttons at top
        vertical_layout = QVBoxLayout()
        vertical_layout.addItem(horizontal_layout)
        vertical_layout.addItem(pen_size_layout)
        vertical_layout.addStretch()

        self.setLayout(vertical_layout)

    def create_color_button(self, color, tooltip):
        # This method creates a button with a specific color and tooltip.
        button = QPushButton()
        button.setStyleSheet(f"background-color: {color}; border: none;")
        button.setToolTip(tooltip)
        button.setFixedSize(50, 50)
        return button
    
    def paintEvent(self, event):
        # Draw the canvas on the widget
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

    def mousePressEvent(self, event):
        # if the left mouse button is pressed, store the position
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

            # Save current canvas state for undo
            self.history.append(self.canvas.copy())

            # limit history size
            if len(self.history) > 20:
                self.history.pop(0)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_point is not None:
            # Draw a line from the last point to the current point
            painter = QPainter(self.canvas)
            pen = QPen(self.current_pen_color, self.current_pen_size, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()  # Trigger repaint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.last_point == event.pos():
                # User clicked without moving — draw a dot
                painter = QPainter(self.canvas)
                pen = QPen(self.current_pen_color, self.current_pen_size, Qt.SolidLine)
                painter.setPen(pen)
                # draw a very short line or a point
                painter.drawPoint(event.pos())
                self.update()
            self.last_point = None

    def resizeEvent(self, event):
        # Create a new canvas with the updated size
        new_canvas = QPixmap(self.size())
        new_canvas.fill(QColor("#141414"))

        # Paint the old canvas onto the new one to preserve drawings
        painter = QPainter(new_canvas)
        painter.drawPixmap(0, 0, self.canvas)
        self.canvas = new_canvas

    def change_pen_color(self, button):
        # if the button is the eraser, set the pen color to the background color
        if button.toolTip() == "Eraser":
            self.current_pen_color = QColor("#141414")
        else:
            # Change the current pen color based on the button clicked
            color = button.styleSheet().split(":")[1].strip().split(";")[0]
            self.current_pen_color = QColor(color)

        # Update the pen style to reflect the new color
        pen = QPen(self.current_pen_color, self.current_pen_size, Qt.SolidLine)
        painter = QPainter(self.canvas)
        painter.setPen(pen)
        self.update()
        self.selectColorButton(button)

    def selectColorButton(self, button):
        # Deselect all buttons
        for btn in self.colour_buttons:
            btn.setStyleSheet(btn.styleSheet().replace("border: 5px solid black;", ""))

        # Select the clicked button
        button.setStyleSheet(button.styleSheet() + "border: 5px solid black;")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z and (event.modifiers() & Qt.ControlModifier):
            self.undo_last_stroke()

    def undo_last_stroke(self):
        if self.history:
            self.canvas = self.history.pop()
            self.update()

    def create_size_button(self, size, tooltip):
        # This method creates a button to select the pen size.
        button = QPushButton(size)
        button.setToolTip(tooltip)
        button.setFixedSize(50, 50)
        button.setStyleSheet("font-size: 16px; color: white;")
        
        return button
    
    def change_pen_size(self, button):
        # Change the pen size based on the button clicked
        self.current_pen_size = int(button.text())
        pen = QPen(self.current_pen_color, self.current_pen_size, Qt.SolidLine)
        painter = QPainter(self.canvas)
        painter.setPen(pen)
        self.update()

        # Deselect all size buttons
        for btn in self.size_buttons:
            btn.setStyleSheet(btn.styleSheet().replace("border: 5px solid black;", ""))

        # Select the clicked button
        button.setStyleSheet(button.styleSheet() + "border: 5px solid black;")

