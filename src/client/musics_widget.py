from PySide6 import QtWidgets, QtCore, QtGui
from src.database.database_models import Musics
import random
import enum
import peewee


class TableRoles(enum.Enum):
    FilePath = QtCore.Qt.ItemDataRole.UserRole


class MusicWidget(QtWidgets.QWidget):
    flag: int = 0
    row: int = 0
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.table = QtWidgets.QTableWidget()
        self.tools_v_layout = QtWidgets.QVBoxLayout()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.main_h_layout.addWidget(self.table)
        self.main_h_layout.addLayout(self.tools_v_layout)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setColumnHidden(2, True)
        
        self.tools_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.table.setHorizontalHeaderLabels(["Исполнитель", "Имя песни"])

        self.table.cellClicked.connect(self.click_cell)
        self.table.currentItemChanged.connect(self.current_item_changed)

        self.fill_musics(Musics.select())
    
    def click_cell(self) -> None:
        if not self.parent.tools_widget.current_music_path:
            self.parent.tools_widget.current_music_path = self.table.model().index(self.table.currentRow(), 2).data()
        
        if self.parent.tools_widget.audio_player.hasAudio() and self.parent.tools_widget.current_music_path == self.parent.tools_widget.new_music_path and self.parent.tools_widget.audio_player.isPlaying():
            self.parent.tools_widget.pause()
            return

        self.parent.tools_widget.play()

    def current_item_changed(self, _: QtWidgets.QTableWidgetItem, __: QtWidgets.QTableWidgetItem) -> None:
        if not self.parent.tools_widget.current_music_path:
            self.parent.tools_widget.current_music_path = self.table.model().index(self.table.currentRow(), 2).data()
        self.parent.tools_widget.new_music_path = self.table.model().index(self.table.currentRow(), 2).data()
        print(self.parent.tools_widget.new_music_path)
    
    def shuffle_items(self) -> list:
        indexes = [(row, column) for row in range(self.table.rowCount()) for column in range(self.table.columnCount())]
        result = [indexes[i:i+self.table.columnCount()] for i in range(0, len(indexes), self.table.columnCount())]
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

    def get_files_for_fill(self, list_files: list[QtCore.QFileInfo]) -> tuple[str]:
        path_to_files = [str(elem.absoluteFilePath()) for elem in list_files]
        names = [elem.fileName().split(' - ') for elem in list_files]
        [elem.append(item) for elem, item in zip(names, path_to_files)]
        return names

    def fill_database(self, names: list[str]) -> None:
        list_not_unique_music = []
        new_names = names.copy()
        for elem in names:
            try:
                Musics.create(author=elem[0], name=elem[1], path=elem[2])
            except peewee.IntegrityError: 
                elem.pop(2)
                list_not_unique_music.append(elem)
                new_names.remove(elem)
                

        if len(list_not_unique_music) > 0:
            self.parent.show_message(
                text=f'This musics are aploaded: {str(list_not_unique_music).replace("[", "").replace("]", "")}',
                error=True
            )

        names.clear()
        print(new_names)

        for name in new_names:
            names.append(Musics.get(Musics.name == name[1]))
        
        return names

    
    def fill_musics(self, music) -> None:
        self.table.setRowCount(len(Musics.select()))
        for model in music:
            for item in [['author', 0], ['name', 1], ['path', 2]]: 
                itemWidget = QtWidgets.QTableWidgetItem(getattr(model, item[0]))
                self.table.setItem(self.row, item[1], itemWidget)
            self.row += 1     

    def clear_database(self) -> None:
        for model in Musics.select():
            model.delete().execute()

    def clear_musics(self) -> None:
        self.parent.tools_widget.stop()
        self.clear_database()
        self.table.clearContents()
        self.row = 0
        self.table.setRowCount(0)

