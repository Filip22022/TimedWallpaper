import sys

from PyQt5.QtWidgets import QApplication

from exe_runner import set_wallpaper
from main_window import MainWindow

# set_wallpaper("C:/Users/filip/Pictures/wallpaper/samurai.png")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
