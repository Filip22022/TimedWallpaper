import random

from PyQt5.QtGui import QColor


def clear_layout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def set_random_background_color(self):
    # Generate random RGB values
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    # Create a QColor with the random RGB values
    color = QColor(red, green, blue)

    # Set the background color of the widget
    self.setStyleSheet(f"background-color: {color.name()};")
