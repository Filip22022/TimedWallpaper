import sys

from PyQt5.QtWidgets import QApplication

from src.main_window import MainWindow

stylesheet = """QMainWindow, QPushButton, QLabel, QScrollArea {
    color: white;
    background-color: #201f29;
}


WallpaperButton {
    min-width: 300px;
}

#WallpaperButtonLabel {
    font-size: 16px;
}

#MessageLabel {
    font-size: 16px;
}

QPushButton {
    border-color: #65AD79;
    border-style: outset;
    border-width: 3px;
    border-radius: 10px;
    padding: 6px;
    min-width: 10em;
}

QPushButton:hover {
    background-color: #2A633A;
}

QPushButton:pressed {
    border-style: inset;
}

QPushButton:disabled {
    background-color: gray;
}

QSlider {
    min-height: 20px;
}

QSlider::groove {
    border: 0px;
    color: #C7E3CF;
    height: 20px;
    border-radius: 10px;
    background-color: white;
}

QSlider::handle {
    background: #65AD79;
    height: 20px;
    width: 10px;
    border-radius: 5px;
}

QSlider::handle:pressed {
    background: #2A633A
}

QScrollBar {
    border-radius: 15px;
    border-width: 3px;
}

QScrollBar::handle {
    background: #65AD79;
    border-radius: 5px;
}

QScrollBar::handle:pressed {
    background: #2A633A;
}
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()

    app.exec()

