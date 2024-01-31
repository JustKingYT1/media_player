from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from src.client.musics_widget import MusicWidget
from src.client.tools_widget import ToolsWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.__init_ui()
        self.__setting_ui()
        self.show()
    
    def __init_ui(self) -> None:
        self.central_widget = QtWidgets.QWidget()
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.music_widget = MusicWidget(self)
        self.tools_widget = ToolsWidget(self)
    
    def __setting_ui(self) -> None:
        self.resize(450, 340)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_v_layout)
        self.main_v_layout.setContentsMargins(0,0,0,0)
        self.main_v_layout.addWidget(self.music_widget)
        self.main_v_layout.addWidget(self.tools_widget)