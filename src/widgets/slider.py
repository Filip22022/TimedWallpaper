from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QHBoxLayout


class Slider(QSlider):
    def __init__(self, minimum, maximum):
        super(Slider, self).__init__(Qt.Horizontal)

        self.setSingleStep(1)
        self.setTickPosition(QSlider.TicksBothSides)
        self.setTickInterval(1)
        self.setMinimum(minimum)
        self.setMaximum(maximum)

