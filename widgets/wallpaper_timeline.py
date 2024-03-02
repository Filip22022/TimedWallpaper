from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QVBoxLayout
from superqt import QRangeSlider

from utilities.functions import clear_layout
from widgets.buttons import WallpaperButton


class WallpaperTimeline(QWidget):
    """
    Custom widget displaying the timeline for choosing wallpapers and wallpaper change times
    """

    def __init__(self):
        super(WallpaperTimeline, self).__init__()
        self.changepoint_count = 2

        self.timeline = Timeline()
        self.display = WallpaperDisplay()
        self.timeline.valuesChanged.connect(self.display.update_times)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.timeline)
        layout.addWidget(self.display)
        self.setLayout(layout)

    def update_changepoints(self, count):
        self.timeline.update_count(count)
        self.update()


class Timeline(QWidget):
    """
    Custom widget providing the timeline with marked hours
    """
    valuesChanged = QtCore.pyqtSignal(list)

    def __init__(self, values=None, count: int = None):
        """
        :param int[] values: starting time values for the sliders in minutes
        :param int count: number of sliders to be displayed
        """
        super(Timeline, self).__init__()
        self._min = 0
        self._max = 24 * 60 - 1
        self._interval = 5
        if values is None:
            values = [6 * 60, 20 * 60]
        self.values = values
        if count is None:
            count = 2
        self.changepoint_count = count
        self._slider = QRangeSlider(Qt.Horizontal)

        levels = range(self._min, self._max + 1, self._interval)
        self._levels = list(zip(levels, map(str, levels)))

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self._setup_slider()

        layout.addWidget(self._slider, stretch=1)
        layout.setAlignment(self._slider, Qt.AlignVCenter)
        layout.setAlignment(self._slider, Qt.AlignTop)
        self.setLayout(layout)

    def _setup_slider(self):
        self._slider.setMinimum(self._min)
        self._slider.setMaximum(self._max)
        self._slider.setValue(self.values)
        self._slider.setTickPosition(QSlider.TicksBelow)
        self._slider.setTickInterval(60)
        self._slider.setSingleStep(self._interval)
        self._slider.setBarMovesAllHandles(False)
        self._slider.valueChanged.connect(self.update_values)

    def update_count(self, count):
        """
        Update the Timeline state to the desired count.

        :param count: the new number of sliders on timeline
        """
        self.changepoint_count = count
        length = len(self.values)

        if self.changepoint_count > len(self.values):
            # New value added between the last two to avoid going out of range
            last_value = self.values[length - 1]
            new_value = last_value - (last_value - self.values[length - 2]) // 2
            self.values.append(new_value)
            self.values.sort()

        # Leave the last slider to save the order
        new_values = self.values[:self.changepoint_count - 1] + self.values[-1:]
        self._slider.setValue(new_values)

    def update_values(self):
        self.values = list(self._slider.value())
        self._emit_values(self.values)
    def _emit_values(self, values):
        self.valuesChanged.emit(values)


class WallpaperDisplay(QWidget):
    """
    Custom widget showing currently chosen wallpapers and allowing changes
    """

    def __init__(self):
        super(WallpaperDisplay, self).__init__()
        self._changepoint_count = 2
        self._changepoints = []
        self._init_ui()

    def _init_ui(self):
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(10, 10, 10, 10)

        self._button_layout = QHBoxLayout()

        self._label_layout = QHBoxLayout()
        self._setup_labels()

        self._layout.addLayout(self._button_layout)
        self._layout.addLayout(self._label_layout, stretch=0)
        self.setLayout(self._layout)

    def _setup_labels(self):
        self._changepoints = []
        for _ in range(self._changepoint_count):
            changepoint = WallpaperButton()
            changepoint.setAlignment(Qt.AlignCenter)
            self._changepoints.append(changepoint)
            self._label_layout.addWidget(changepoint)

    def _update_labels(self):
        clear_layout(self._label_layout)
        self._setup_labels()
        self._update_times()

    def update_count(self, count):
        self._changepoint_count = count

    def update_times(self, values):
        last_value = values[-1]
        for changepoint, value in zip(self._changepoints, values):
            changepoint.setTimes(last_value, value)
            last_value = value
