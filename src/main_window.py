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
        self.resize(900, 600)

        self.changepoint_count = 2
        self.wallpaper_timeline = WallpaperTimeline()
        self.msg = QMessageBox()

        self.text_label = QLabel("Number of daily changes:")
        self.counter_label = QLabel("2")

        self.plus_button = CounterButton("+", self)
        self.plus_button.clicked.connect(self.changepoint_increment)
        self.minus_button = CounterButton("-", self)
        self.minus_button.clicked.connect(self.changepoint_decrement)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_wallpapers)
        self.disable_button = QPushButton("Disable script")
        self.disable_button.clicked.connect(self.terminate_script)

        self._init_ui()

    def _init_ui(self):

        self.counter_label.setStyleSheet('border: 2px solid black; padding: 5px;')
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
        self.confirm_button.setDisabled(Process.file_exists())
        button_layout.addWidget(self.disable_button)
        button_layout.setAlignment(self.disable_button, Qt.AlignLeft)
        self.disable_button.setEnabled(Process.file_exists())

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(counter_layout, stretch=1)
        main_layout.addWidget(self.wallpaper_timeline, stretch=2)
        main_layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

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
            data = self.wallpaper_timeline.get_data()
        except Exception as e:
            show_message(str(e))
            return
        WallpaperData.save(data)

        exe_path = app_root_path("./executable/wallpaper_switcher.exe")

        process = subprocess.Popen([exe_path])

        pid = process.pid
        print("Proces started with pid: " + str(pid))
        Process.save(pid)

        self.disable_button.setEnabled(Process.file_exists())
        self.confirm_button.setDisabled(Process.file_exists())

    def terminate_script(self):
        if Process.file_exists():
            if Process.is_active():
                Process.terminate()
                Process.remove_file()
            else:
                Process.remove_file()
        else:
            raise Exception("No saved process")

        self.disable_button.setEnabled(Process.file_exists())
        self.confirm_button.setDisabled(Process.file_exists())


def show_message(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("Message")
    msg.setStandardButtons(QMessageBox.Ok)

    # Execute the message box
    msg.exec_()
