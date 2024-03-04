from collections import namedtuple

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QVBoxLayout, QScrollArea
from superqt import QRangeSlider

from src.utilities.WallpaperData import WallpaperData
from src.widgets.buttons import WallpaperButton


class WallpaperTimeline(QWidget):
    """
    Custom widget displaying the timeline for choosing wallpapers and wallpaper change times
    """

    def __init__(self):
        super(WallpaperTimeline, self).__init__()

        default_times = [6 * 60, 20 * 60]
        default_count = len(default_times)
        self.timeline = Timeline(default_times, default_count)
        self.display = WallpaperDisplay()
        self.display.set_times(self.timeline.get_hours())
        self.timeline.valuesChanged.connect(self.display.set_times)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.timeline)

        # Enable horizontal scrolling on timeline widget
        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setStyleSheet("border: None;")
        self.scroll.setWidget(self.display)

        layout.addWidget(self.scroll, stretch=1)
        self.setLayout(layout)

    def update_changepoints(self, count):
        self.timeline.update_count(count)
        self.display.update_count(count)
        self.display.set_times(self.timeline.get_hours())
        self.update()

    def get_data(self):
        values = self.timeline.get_hours()
        paths = self.display.get_images()
        return [WallpaperData(value, path) for value, path in zip(values, paths)]


class Timeline(QWidget):
    """
    Custom widget providing the timeline with marked hours
    """
    valuesChanged = QtCore.pyqtSignal(list)

    def __init__(self, values: list[int], display_count: int):
        """
        :param list[int] values: starting time values for the sliders in minutes
        :param int display_count: number of sliders to be displayed
        """
        super(Timeline, self).__init__()
        self._min = 0
        self._max = 24 * 60 - 1
        self._interval = 5
        self.values = values
        self.changepoint_count = display_count
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
        self._slider.valueChanged.connect(self._update_values)

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

    def _update_values(self):
        self.values = list(self._slider.value())
        self._emit_values(self.get_hours())

    def _emit_values(self, values):
        self.valuesChanged.emit(values)

    def get_hours(self):
        hours = [str(int(val // 60)) for val in self.values]
        minutes = [str(int(val % 60)) for val in self.values]
        return [str(h + ":" + m) for h, m in zip(hours, minutes)]


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
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._create_changepoints(self._changepoint_count)

        self.setLayout(self._layout)

    def _create_changepoints(self, number):
        for _ in range(number):
            changepoint = WallpaperButton()
            changepoint.setAlignment(Qt.AlignCenter)
            self._changepoints.append(changepoint)
            self._layout.addWidget(changepoint)

    def update_count(self, count):
        self._changepoint_count = count
        if len(self._changepoints) < self._changepoint_count:
            needed = self._changepoint_count - len(self._changepoints)
            self._create_changepoints(needed)
        if len(self._changepoints) >= self._changepoint_count:
            for i in range(self._changepoint_count):
                self._changepoints[i].show()
            for i in range(self._changepoint_count, len(self._changepoints)):
                self._changepoints[i].hide()

    def set_times(self, values):
        last_value = values[-1]
        for changepoint, value in zip(self._changepoints, values):
            changepoint.setTimes(last_value, value)
            last_value = value

    def get_images(self):
        image_paths = []
        for c in self._changepoints:
            image_paths.append(c.path)
        return image_paths
