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
            self.parent.stop_flag = True
            self.grabMouse()
        elif event.type() == QtCore.QEvent.MouseButtonRelease and source is self:
            self.releaseMouse()
            self.set_new_audio_code()
        elif event.type() == QtCore.QEvent.MouseMove and source is self:
            if self.isSliderDown():
                cursor_position = event.globalPos()
                slider_position = self.mapFromGlobal(cursor_position)
                value = self.minimum() + (self.maximum() - self.minimum()) * slider_position.x() / self.width()
                self.setValue(int(value))
        return super().eventFilter(source, event)

    def get_new_time_code(self) -> None:
        return (int(self.parent.total_time.split(':')[0]) * 60 + int(self.parent.total_time.split(':')[1])) / 100 * self.value()
    
    def set_new_audio_code(self) -> None:
        new_time_code = self.get_new_time_code() * 1000
        self.parent.parent.audio_player.setPosition(int(new_time_code))
        self.parent.stop_flag = False