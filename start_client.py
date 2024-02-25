from sys import argv, path
from settings import *

path.append('C:/media_player/')

from src.client.main_window import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(argv)
    root = MainWindow()
    app.exec()