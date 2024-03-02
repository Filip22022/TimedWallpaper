from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, \
    QMessageBox

from widgets.buttons import CounterButton
from widgets.wallpaper_timeline import WallpaperTimeline


class MultiSlider:
    pass


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        self.resize(900, 600)

        self.changepoint_count = 2
        self.wallpaper_timeline = WallpaperTimeline()
        self.msg = QMessageBox()

        self.label = QLabel("2")
        self._setup_label()

        self.plus_button = CounterButton("+", self)
        self.plus_button.clicked.connect(self.changepoint_increment)
        self.minus_button = CounterButton("-", self)
        self.minus_button.clicked.connect(self.changepoint_decrement)

        self._init_ui()

    def _init_ui(self):
        # Create counter layout
        counter_layout = QHBoxLayout()
        counter_layout.addWidget(self.label, stretch=0)
        counter_layout.setAlignment(self.label, Qt.AlignCenter)
        counter_layout.addWidget(self.plus_button)
        counter_layout.addWidget(self.minus_button)
        counter_layout.setAlignment(self.minus_button, Qt.AlignLeft)
        counter_layout.setAlignment(self.plus_button, Qt.AlignLeft)
        counter_layout.addStretch(10)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(counter_layout, stretch=1)
        main_layout.addWidget(self.wallpaper_timeline, stretch=2)

        widget = QWidget()
        widget.setLayout(main_layout)
        # Enable horizontal scrolling
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.setCentralWidget(scroll)

    def _setup_label(self):
        self.label.setContentsMargins(30, 5, 10, 5)
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)

    def changepoint_count_change(self):
        self.label.setNum(self.changepoint_count)
        self.wallpaper_timeline.update_changepoints(self.changepoint_count)

    def changepoint_decrement(self):
        if self.changepoint_count > 2:
            self.changepoint_count -= 1
            self.changepoint_count_change()
        else:
            self.msg.setText("Minimum changepoint number is 2")
            self.msg.exec()

    def changepoint_increment(self):
        if self.changepoint_count < 9:
            self.changepoint_count += 1
            self.changepoint_count_change()
        else:
            self.msg.setText("Maximum changepoint number is 9")
            self.msg.exec()
