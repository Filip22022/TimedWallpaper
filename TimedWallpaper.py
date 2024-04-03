import sys

from PyQt5.QtWidgets import QApplication

from src.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("stylesheet.qss", "r") as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()

    app.exec()

