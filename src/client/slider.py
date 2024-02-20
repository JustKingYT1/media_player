from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QMouseEvent


class Slider(QtWidgets.QSlider):
    current_slide_seconds = 0
    def __init__(self, parent, orientation: QtCore.Qt.Orientation, style: str) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__setting_ui(orientation, style)
    
    def __setting_ui(self, orientation: QtCore.Qt.Orientation, style: str) -> None:
        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(100)
        self.installEventFilter(self)
        self.setOrientation(orientation)
        self.setStyleSheet(style)
    
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and source is self:
            self.grabMouse()
            cursor_position = event.globalPos()
            slider_position = self.mapFromGlobal(cursor_position)
            value = self.minimum() + (self.maximum() - self.minimum()) * slider_position.x() / self.width()
            self.setValue(int(value))
        elif event.type() == QtCore.QEvent.MouseButtonRelease and source is self:
            self.releaseMouse()
        elif event.type() == QtCore.QEvent.MouseMove and source is self:
            if self.isSliderDown():
                cursor_position = event.globalPos()
                slider_position = self.mapFromGlobal(cursor_position)
                value = self.minimum() + (self.maximum() - self.minimum()) * slider_position.x() / self.width()
                self.setValue(int(value))
        return super().eventFilter(source, event)