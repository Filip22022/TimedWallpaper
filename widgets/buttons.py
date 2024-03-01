from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy


class CounterButton(QPushButton):
    def __init__(self, text, parent=None):
        super(CounterButton, self).__init__(text, parent)
        self.setMaximumWidth(100)
        self.setMaximumHeight(80)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        font = QFont()
        font.setPointSize(20)
        self.setFont(font)


class ImageButton(QPushButton):
    def __init__(self, parent=None):
        super(ImageButton, self).__init__("Choose Image", parent)
        self.image = None

    def setImage(self, image_path):
        self.setText("")
        self.image = image_path
        self.setIcon(QtGui.QIcon(image_path))
        self.setIconSize(self.size())
        self.update()
