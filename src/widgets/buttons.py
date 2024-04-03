import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QFileDialog, QLabel, QVBoxLayout, QWidget

from src.storage.functions import save_image, app_root_path


class WallpaperButton(QWidget):
    """
    Custom widget providing a label with attached choose image button below
    """

    def __init__(self):
        super(WallpaperButton, self).__init__()
        self.layout = QVBoxLayout()
        self.path = None
        self.label = QLabel()
        self.label.setObjectName("WallpaperButtonLabel")
        self.image_button = ImageButton()
        self.min_size = QSize(400, 300)
        self.max_size = QSize(800, 600)

        self.image_button.clicked.connect(self._choose_image)

        self._init_ui()

    def _init_ui(self):
        self.label.setContentsMargins(5, -5, 5, 5)
        self.label.setMaximumSize(self.max_size)
        self.image_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_button.setMinimumSize(self.min_size)
        self.image_button.setMaximumSize(self.max_size)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.image_button, stretch=1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def _choose_image(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Images (*.png *.jpg)")

        img_directory = app_root_path(".\data\images")
        os.makedirs(img_directory, exist_ok=True)
        dialog.setDirectory(img_directory)
        if dialog.exec():
            file_path = dialog.selectedFiles()
            saved_path = save_image(file_path[0])
            self.path = saved_path
            self.image_button.setImage(self.path)

    def setAlignment(self, alignment):
        self.label.setAlignment(alignment)

    def setTimes(self, time_start, time_end):
        self.label.setText(time_start + ' - ' + time_end)

    def set_image(self, image_path):
        self.path = image_path
        self.image_button.setImage(self.path)


class CounterButton(QPushButton):
    def __init__(self, text, parent=None):
        super(CounterButton, self).__init__(text, parent)
        self.setMaximumWidth(100)
        self.setMaximumHeight(80)

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

        # setting image to the button
        self.setStyleSheet(f"border-image : url({self.image});")
        self.update()
