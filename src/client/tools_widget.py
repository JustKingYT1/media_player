from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget


class ToolsWidget(QtWidgets.QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.listen_button = QtWidgets.QPushButton(text='Listen')
        self.stop_button = QtWidgets.QPushButton(text='Stop')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)

        self.main_h_layout.addWidget(self.listen_button)
        self.main_h_layout.addWidget(self.stop_button)
        