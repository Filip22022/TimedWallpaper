from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QFileDialog, QLabel, QVBoxLayout, QWidget


class WallpaperButton(QWidget):
    """
    Custom widget providing a label with attached choose image button below
    """

    def __init__(self):
        super(WallpaperButton, self).__init__()
        self.layout = QVBoxLayout()
        self.path = None

        self.label = QLabel()
        self.label.setContentsMargins(5, -5, 5, 5)
        self.image_button = ImageButton()
        self.image_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_button.clicked.connect(self.choose_image)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.image_button, stretch=1)
        self.setLayout(self.layout)

    def choose_image(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Images (*.png *.jpg)")
        if dialog.exec():
            file_path = dialog.selectedFiles()
            self.path = file_path[0]
            self.image_button.setImage(self.path)

    def setAlignment(self, alignment):
        self.label.setAlignment(alignment)
        # self.layout.setAlignment(self.image_button, Qt.AlignCenter)

    def setText(self, text):
        self.label.setText(text)


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
