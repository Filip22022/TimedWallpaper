from PyQt5.QtCore import QSize
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
        if dialog.exec():
            file_path = dialog.selectedFiles()
            self.path = file_path[0]
            self.image_button.setImage(self.path)

    def setAlignment(self, alignment):
        self.label.setAlignment(alignment)

    def setTimes(self, time_start_minutes, time_end_minutes):
        start_hours_minutes = str(int(time_start_minutes // 60)) + ":" + str(int(time_start_minutes % 60))
        end_hours_minutes = str(int(time_end_minutes // 60)) + ":" + str(int(time_end_minutes % 60))
        self.label.setText(start_hours_minutes + " - " + end_hours_minutes)


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
        self.setStyleSheet(f"border-image : url({self.image}); background-size: cover;")
        self.update()
