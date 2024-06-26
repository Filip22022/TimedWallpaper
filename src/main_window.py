import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton

from src.storage.data import WallpaperData
from src.storage.functions import app_root_path
from src.storage.process import Process
from src.widgets.buttons import CounterButton
from src.widgets.wallpaper_timeline import WallpaperTimeline


class MainWindow(QMainWindow):

    # noinspection PyUnresolvedReferences
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        self.resize(1000, 700)

        self.text_label = QLabel("Number of daily changes:")
        self.counter_label = QLabel("2")
        self.message_label = QLabel("")
        self.message_label.setObjectName("MessageLabel")

        self.changepoint_count = 2
        self.wallpaper_timeline = WallpaperTimeline()
        self.load_data()
        self.msg = QMessageBox()

        self.plus_button = CounterButton("+", self)
        self.plus_button.clicked.connect(self.changepoint_increment)
        self.minus_button = CounterButton("-", self)
        self.minus_button.clicked.connect(self.changepoint_decrement)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_wallpapers)
        self.disable_button = QPushButton("Disable")
        self.disable_button.clicked.connect(self.terminate_script)

        self._init_ui()

    def _init_ui(self):
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setContentsMargins(30, 20, 30, 20)
        font = QFont()
        font.setPointSize(20)
        self.counter_label.setFont(font)
        font.setPointSize(12)
        self.text_label.setFont(font)

        # Create counter layout
        counter_layout = QHBoxLayout()
        counter_layout.addStretch(2)
        counter_layout.addWidget(self.text_label)
        counter_layout.addWidget(self.counter_label)
        counter_layout.addWidget(self.plus_button)
        counter_layout.addWidget(self.minus_button)
        counter_layout.addStretch(2)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.confirm_button)
        button_layout.setAlignment(self.confirm_button, Qt.AlignRight)
        self.confirm_button.setDisabled(Process.is_active())
        button_layout.addWidget(self.disable_button)
        button_layout.setAlignment(self.disable_button, Qt.AlignLeft)
        self.disable_button.setEnabled(Process.is_active())

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(counter_layout, stretch=1)
        main_layout.addWidget(self.wallpaper_timeline, stretch=2)
        main_layout.addLayout(button_layout)

        main_layout.addWidget(self.message_label)
        main_layout.setAlignment(self.message_label, Qt.AlignHCenter)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def load_data(self):
        if WallpaperData.has_saved_data():
            loaded_data = WallpaperData.load()
            self.wallpaper_timeline.load(loaded_data)
            self.changepoint_count = len(loaded_data)
            self.counter_label.setNum(self.changepoint_count)
        if Process.is_active():
            self.message_label.setText("Background script running")
        else:
            self.message_label.setText("No script active")

    def changepoint_count_change(self):
        self.counter_label.setNum(self.changepoint_count)
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

    def confirm_wallpapers(self):
        try:
            times, images = self.wallpaper_timeline.get_data()
            WallpaperData.save(times, images)
        except Exception as e:
            show_message(str(e))
            return

        self.start_switcher()

        if Process.is_active():
            self.message_label.setText("Background script running")

            self.disable_button.setEnabled(Process.is_active())
            self.confirm_button.setDisabled(Process.is_active())
        else:
            show_message("Failed to start script")

    def start_switcher(self):
        self.message_label.setText("Script starting")

        exe_path = app_root_path("./wallpaper_switcher.exe")

        process = subprocess.Popen([exe_path])

        pid = process.pid
        print("Proces started with pid: " + str(pid))

    def terminate_script(self):
        if Process.is_active():
            Process.terminate()
        else:
            show_message("No process running")

        self.disable_button.setEnabled(Process.is_active())
        self.confirm_button.setDisabled(Process.is_active())
        self.message_label.setText("No script active")


def show_message(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("Message")
    msg.setStandardButtons(QMessageBox.Ok)

    # Execute the message box
    msg.exec_()
