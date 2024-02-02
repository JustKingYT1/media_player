from PySide6 import QtWidgets, QtCore, QtGui
from src.database.database_models import Musics
import random


class MusicWidget(QtWidgets.QWidget):
    flag: int = 0
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.table = QtWidgets.QTableWidget()
        self.tools_v_layout = QtWidgets.QVBoxLayout()
        self.switch_button = QtWidgets.QPushButton(text='Show')
        self.random_button = QtWidgets.QPushButton(text='Randomize')
        self.table.setCurrentCell(2, 1)

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.main_h_layout.addWidget(self.table)
        self.main_h_layout.addLayout(self.tools_v_layout)
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        
        self.tools_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.tools_v_layout.addWidget(self.switch_button)
        self.tools_v_layout.addWidget(self.random_button)

        self.table.setHorizontalHeaderLabels(["Имя песни", "Исполнитель", "Время"])

        self.switch_button.clicked.connect(self.switch_function)
        self.random_button.clicked.connect(self.randomize)
    
    def switch_function(self) -> None:
        match self.flag:
            case 0: 
                self.fill_musics()
                self.flag = 1
            case 1: 
                self.clear_musics()
                self.flag = 0
    
    def shuffle_items(self) -> list:
        self.rows = self.table.rowCount()
        self.columns = self.table.columnCount()
        indexes = [(row, column) for row in range(self.rows) for column in range(self.columns)]
        result = [indexes[i:i+3] for i in range(0, len(indexes), 3)]
        random.shuffle(result)
        return result


    def randomize(self) -> None:
        new_rows = random.sample(range(0, self.table.rowCount()), self.table.rowCount())
        for row, new_row in zip(self.shuffle_items(), new_rows):
            for attr in row:
                old_row = attr[0]
                old_column = attr[1]
                old_item = self.table.takeItem(old_row, old_column)
                new_column = attr[1]
                new_item = self.table.takeItem(new_row, new_column)
                self.table.setItem(old_row, old_column, new_item)
                self.table.setItem(new_row, new_column, old_item)
    
    def fill_musics(self) -> None:
        count = 0
        self.table.setRowCount(len(Musics.select()))
        for model in Musics.select():
            for item in [['author', 0], ['name', 1], ['time', 2]]: 
                self.table.setItem(count, item[1], QtWidgets.QTableWidgetItem(getattr(model, item[0])))
            count += 1
        self.parent.tools_widget.next_button.setEnabled(True)
        self.parent.tools_widget.previous_button.setEnabled(True)            
        self.switch_button.setText('Hide')

    def clear_musics(self) -> None:
        self.table.clearContents()
        self.table.setRowCount(0)
        self.parent.tools_widget.next_button.setEnabled(False)
        self.parent.tools_widget.previous_button.setEnabled(False)
        self.switch_button.setText('Show')
