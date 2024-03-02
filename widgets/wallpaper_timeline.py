from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QSizePolicy
from superqt import QRangeSlider

from utilities.functions import clear_layout
from widgets.buttons import ImageButton


class WallpaperTimeline(QWidget):
    """
    Custom widget displaying the timeline for choosing wallpapers and wallpaper change times
    """

    def __init__(self):
        super(WallpaperTimeline, self).__init__()
        self.changepoint_count = 2

        layout = QVBoxLayout()
        self.timeline = Timeline()
        layout.addWidget(self.timeline)
        self.setLayout(layout)

    def update_changepoints(self, count):
        self.timeline.update_values(count)
        self.update()


class Timeline(QWidget):
    """
    Custom widget providing the timeline with marked hours
    """

    def __init__(self, values=None, count: int = None):
        """
        :param int[] values: starting time values for the sliders in minutes
        :param int count: number of sliders to be displayed
        """
        super(Timeline, self).__init__()

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(10, 10, 10, 10)

        self._min = 0
        self._max = 24 * 60 - 1
        self._interval = 5
        if values is None:
            values = [6 * 60, 20 * 60]
        self.values = values
        if count is None:
            count = 2
        self.changepoint_count = count

        levels = range(self._min, self._max + 1, self._interval)
        self._levels = list(zip(levels, map(str, levels)))

        self._images = []
        self._image_layout = QHBoxLayout()

        self._slider = None
        self._setup_slider()

        self._changepoints = []
        self._label_layout = QHBoxLayout()
        self._setup_labels()
        self._update_label_values()

        self._layout.addLayout(self._image_layout)
        self._layout.addWidget(self._slider, stretch=0)
        self._layout.setAlignment(self._slider, Qt.AlignVCenter)
        self._layout.setAlignment(self._slider, Qt.AlignTop)
        self._layout.addLayout(self._label_layout, stretch=0)
        self.setLayout(self._layout)

    def _setup_slider(self):
        self._slider = QRangeSlider(Qt.Horizontal)
        self._slider.setMinimum(self._min)
        self._slider.setMaximum(self._max)
        self._slider.setValue(self.values)
        self._slider.setTickPosition(QSlider.TicksBelow)
        self._slider.setTickInterval(60)
        self._slider.setSingleStep(self._interval)
        self._slider.setBarMovesAllHandles(False)
        self._slider.valueChanged.connect(self._update_label_values)

    def _setup_labels(self):
        self._changepoints = []
        for _ in self.values[0:self.changepoint_count]:
            changepoint = WallpaperButton()
            changepoint.setAlignment(Qt.AlignCenter)
            self._changepoints.append(changepoint)
            self._label_layout.addWidget(changepoint)

    def _update_labels(self):
        clear_layout(self._label_layout)
        self._setup_labels()
        self._update_label_values()

    def _update_label_values(self):
        self.values = list(self._slider.value())
        for label, value in zip(self._changepoints, self.values):
            label.setText(str(int(value // 60)) + ":" + str(int(value % 60)))

    def update_values(self, count):
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
        self._update_labels()

