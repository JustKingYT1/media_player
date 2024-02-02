from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QMouseEvent


class Slider(QtWidgets.QSlider):
    current_slide_seconds = 0
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(100)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        minutes = int(self.parent.total_time.split(':')[0])
        seconds = int(self.parent.total_time.split(':')[1])
        total_seconds = minutes * 60 + seconds
        self.current_slide_seconds = total_seconds * self.value() / 100
        print(self.current_slide_seconds)