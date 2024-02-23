from PySide6 import QtWidgets, QtCore, QtGui
from src.database.database_models import Musics
import random
import enum
import peewee
import eyed3
import io
import typing


class TypesData(enum.Enum):
    ImgRole: int = 1001

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
        loaded_files = sorted([eyed3.load(file) for file in path_to_files], key=lambda x: x.tag.title)
        
        return loaded_files

    def fill_database(self, loaded_files: list[eyed3.AudioFile]) -> None:
        list_not_unique_music = [] 
        new_names = loaded_files.copy()
        for item in loaded_files:
            try:
                Musics.create(artist=item.tag.artist, title=item.tag.title, path=item.path)
            except peewee.IntegrityError: 
                list_not_unique_music.append(f'{item.tag.artist} - {item.tag.title}')
                new_names.remove(item)
                

        if len(list_not_unique_music) > 0:
            self.parent.show_message(
                text=f'This musics are aploaded: {str(list_not_unique_music).replace("[", "").replace("]", "")}',
                error=True
            )

        loaded_files.clear()

        for item in new_names:
            loaded_files.append(Musics.get(Musics.title == item.tag.title))
        
        return loaded_files

    
    def fill_musics(self, musics: list[eyed3.AudioFile] | typing.Any) -> None:
        self.table.setRowCount(len(Musics.select()))
        for model in musics:
            for item in [['artist', 0], ['title', 1], ['path', 2]]: 
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
        self.table.setRowCount(0)
        self.row = 0

