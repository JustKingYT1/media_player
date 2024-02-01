from PySide6.QtWidgets import *
from PySide6.QtCore import *

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
        self.progress_bar = QProgressBar(value=0)
        self.timer = QTimer(self)

    def __setup_ui(self) -> None:
        self.setLayout(self.main_h_layout)

        self.progress_bar.setFormat("")
        
        self.main_h_layout.addWidget(self.current_time_label)
        self.main_h_layout.addWidget(self.progress_bar)
        self.main_h_layout.addWidget(self.total_time_label)

        self.timer.timeout.connect(self.update_time)

    def get_total_time(self) -> str:
        total_frames = self.parent.tools_widget.wf.getnframes()
        frame_rate = self.parent.tools_widget.wf.getframerate()
        
        total_duration = total_frames / frame_rate

        total_minutes = total_duration // 60
        total_seconds = total_duration % 60
        return f'{int(total_minutes)}:{int(total_seconds):02d}'   
    
    def get_current_time(self) -> str:
        current_minutes = self.parent.tools_widget.current_time // 60
        current_seconds = self.parent.tools_widget.current_time % 60
        return f'{int(current_minutes)}:{int(current_seconds):02d}'

    def update_time(self):
        self.total_time_label.setText(self.get_total_time())
        self.current_time_label.setText(self.get_current_time())
        self.progress_bar.setValue((self.parent.tools_widget.chunk_total/self.parent.tools_widget.wf.getnframes())*100)
        