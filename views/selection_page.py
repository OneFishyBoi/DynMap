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

        # counter for number of maps
        self.map_count = 0

        # current selected map
        self.current_map = None

        # Set grid layout inside mini_background
        self.grid_layout = QGridLayout(self.mini_background)

        # button to add new maps
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.add_button_clicked)
        self.grid_layout.addWidget(self.add_button, 0, 0)

        # styling button
        self.add_button.setStyleSheet("""
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
        self.grid_layout.addWidget(QLabel(""), 0, 1)
        self.grid_layout.addWidget(QLabel(""), 0, 2)
        self.grid_layout.addWidget(QLabel(""), 1, 0)
        self.grid_layout.addWidget(QLabel(""), 2, 0)

        # adding delete button and open button
        bin_button = QPushButton("BIN")
        open_button = QPushButton("OPEN")
        bin_button.clicked.connect(self.remove_selected_map)

        # styling both buttons
        for button in (bin_button, open_button):
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
        right_box.addWidget(bin_button)

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

    def add_button_clicked(self):
        # Move the add button to new position
        # calc the new pos
        new_x = (self.map_count + 1) % 3
        new_y = (self.map_count + 1) // 3

        # Remove any widget already in that position
        existing_item = self.grid_layout.itemAtPosition(new_y, new_x)
        if existing_item is not None:
            widget = existing_item.widget()
            if widget:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()

        # moving add button to new position
        self.grid_layout.addWidget(self.add_button, new_y, new_x)

        # Add the new map to the grid layout
        new_map = QPushButton("Map {}".format(self.map_count + 1))
        new_map.setStyleSheet("""
            QPushButton {
                border: 2px solid white;
                border-radius: 6px;
                font-size: 20px;
                color: white;
                background-color: #444;
                height: 300px;
            }
            QPushButton:hover {
                border-color: cyan;
            }
        """)
        new_x = (self.map_count) % 3
        new_y = (self.map_count) // 3
        self.grid_layout.addWidget(new_map, new_y, new_x)

        # adding logic for selecting the map
        new_map.clicked.connect(lambda checked, btn=new_map: self.select_map_button(btn))
        new_map.clearFocus()
        
        # Increment the map count
        self.map_count += 1

    def showEvent(self, event):
        super().showEvent(event)

        # Only run once
        if not hasattr(self, '_mini_background_fixed'):
            initial_width = self.mini_background.width()
            initial_height = self.mini_background.height()
            self.mini_background.setFixedSize(initial_width, initial_height)
            self._mini_background_fixed = True

    def select_map_button(self, button):
        # Reset previously selected button
        if self.current_map:
            self.current_map.setStyleSheet("""
                QPushButton {
                    border: 2px solid white;
                    border-radius: 6px;
                    font-size: 20px;
                    color: white;
                    background-color: #444;
                    height: 300px;
                }
                QPushButton:hover {
                    border-color: cyan;
                }
            """)

        # Set new selected button
        button.setStyleSheet("""
            QPushButton {
                border: 2px solid cyan;
                border-radius: 6px;
                font-size: 20px;
                color: white;
                background-color: #444;
                height: 300px;
            }
            QPushButton:hover {
                border-color: cyan;
            }
        """)
        self.current_map = button

    def remove_selected_map(self):
        if self.current_map:
            # Find the position of the current map
            for i in range(self.grid_layout.rowCount()):
                for j in range(self.grid_layout.columnCount()):
                    item = self.grid_layout.itemAtPosition(i, j)
                    if item and item.widget() == self.current_map:
                        # Remove the widget and reset the position
                        self.grid_layout.removeWidget(self.current_map)
                        self.grid_layout.addWidget(QLabel(""), i, j)
                        self.current_map.deleteLater()
                        self.current_map = None
                        self.map_count -= 1
                        self.reload_maps()
                        return
    
    def reload_maps(self):
        maps = []
        # Clear the grid layout and get list of current maps
        for i in range(self.grid_layout.rowCount()):
            for j in range(self.grid_layout.columnCount()):
                item = self.grid_layout.itemAtPosition(i, j)
                if item:
                    widget = item.widget()
                    # if the widget is a QPushButton, it is a map button
                    # if the widget is a QLabel, it is an empty space
                    # therefore, remove the QPushButton and add a QLabel in its place
                    if isinstance(widget, QPushButton):
                        maps.append(widget)
                        self.grid_layout.removeWidget(widget)
                        self.grid_layout.addWidget(QLabel(""), i, j)

        # reset map count
        self.map_count = 0
        self.current_map = None

        # Re-add the all maps to the grid layout
        # add all maps to the grid layout
        for map in maps:
            self.add_map(map)
        
        # reduce map count for the add button
        self.map_count -= 1

    def add_map(self, map):
        # Add the map button to the grid layout
        new_x = (self.map_count) % 3
        new_y = (self.map_count) // 3

        # Remove placeholder QLabel if it exists
        existing_item = self.grid_layout.itemAtPosition(new_y, new_x)
        if existing_item is not None:
            widget = existing_item.widget()
            if widget:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()
        self.grid_layout.addWidget(map, new_y, new_x)
        self.map_count += 1

