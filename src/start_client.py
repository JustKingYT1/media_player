from sys import argv, path

path.append('../media_player')

from src.client.main_window import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(argv)
    root = MainWindow()
    app.exec()