from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtGui, QtCore
from src.client.slider import Slider
from PySide6.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout
from PySide6.QtCore import Qt, QPoint

class AudioTimeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setup_ui()
        self.show()

    def __init_ui(self) -> None:
        self.main_h_layout = QHBoxLayout()
        self.current_time_label = QLabel(text='0:00')
        self.total_time_label = QLabel(text='0:00')
        self.slider = Slider(parent=self)
        self.mouse_press_pos = QPoint()
        self.calculate_timer = QTimer(self)
        self.update_timer = QTimer(self)

    def __setup_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        
        self.slider.setOrientation(Qt.Orientation.Horizontal)

        style = """
            QSlider::handle:horizontal {
                width: 5px; /* Ширина ползунка */
                height: 6px; /* Высота ползунка */
                margin: -3px 0; /* Выравнивание ползунка */
                background: #000000; /* Цвет ползунка */
                border-radius: 2px; /* Скругление углов ползунка */
            }

            QSlider::groove:horizontal {
                height: 10px; /* Высота "борозды" ползунка */
                background: #808080; /* Цвет "борозды" ползунка */
                border-radius: 3px; /* Скругление углов "борозды" ползунка */
            }
        """
        self.slider.setStyleSheet(style)

        self.main_h_layout.addWidget(self.current_time_label)
        self.main_h_layout.addWidget(self.slider)
        self.main_h_layout.addWidget(self.total_time_label)

        self.slider.installEventFilter(self)

        self.calculate_timer.timeout.connect(self.calculate_time)
        self.calculate_timer.timeout.connect(self.update_time)

    def get_total_time(self) -> str:
        total_frames = self.parent.tools_widget.wf.getnframes()
        frame_rate = self.parent.tools_widget.wf.getframerate()
        
        total_duration = total_frames / frame_rate

        total_minutes = total_duration // 60
        total_seconds = total_duration % 60
        return f'{int(total_minutes)}:{int(total_seconds):02d}'   

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and source is self.slider:
            self.slider.grabMouse()
        elif event.type() == QtCore.QEvent.MouseButtonRelease and source is self.slider:
            self.slider.releaseMouse()
            self.parent.tools_widget.set_start_time()
        elif event.type() == QtCore.QEvent.MouseMove and source is self.slider:
            if self.slider.isSliderDown():
                cursor_position = event.globalPos()
                slider_position = self.mapFromGlobal(cursor_position)
                value = self.slider.minimum() + (self.slider.maximum() - self.slider.minimum()) * slider_position.x() / self.width()
                self.slider.setValue(int(value))
        return super().eventFilter(source, event)
    
    def get_current_time(self) -> str:
        current_minutes = self.parent.tools_widget.current_time // 60
        current_seconds = self.parent.tools_widget.current_time % 60
        return f'{int(current_minutes)}:{int(current_seconds):02d}'
    
    def calculate_time(self) -> None:
        self.total_time = self.get_total_time()
        self.current_time = self.get_current_time()
        self.total_time_label.setText(self.total_time)
        self.current_time_label.setText(self.current_time)

    def update_time(self) -> None:
        self.slider.setValue((self.parent.tools_widget.chunk_total/self.parent.tools_widget.wf.getnframes())*100)
        