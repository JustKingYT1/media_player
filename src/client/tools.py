from PySide6 import QtGui, QtWidgets, QtCore
import settings


class WorkerThread(QtCore.QThread):
    finished = QtCore.Signal()

    def __init__(self, func, *args, **kwargs) -> None:
        super(WorkerThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self) -> None:
        self.func(*self.args, **self.kwargs)
        self.finished.emit()

def get_pixmap(name: str) -> None:
    return QtGui.QPixmap(f'{settings.IMG_DIR}/{name}.png')


def switch_widgets(widgets: dict[QtWidgets.QWidget], switch: bool):
    for key, widget in widgets.items():
        if isinstance(widget, QtWidgets.QWidget):
            widget.show() if switch else widget.hide()