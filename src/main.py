import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow

# set_wallpaper("C:/Users/filip/Pictures/wallpaper/samurai.png")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
