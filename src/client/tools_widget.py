from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui, QtMultimedia
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from src.client.audio_timer_widget import AudioTimeWidget
from src.settings import IMG_DIR
import time
from src.client.volume_dialog import VolumeSliderDialog

def get_pixmap(name: str) -> None:
    return QtGui.QPixmap(f'{IMG_DIR}/{name}.png')

class ToolsWidget(QtWidgets.QWidget):
    volume_dialog: VolumeSliderDialog = None
    stop_flag: bool = False
    current_time = 0
    index_row = -1
    new_music_path: str = None
    current_music_path: str = None
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.audio_metadata = None
        self.buttons_h_layout = QtWidgets.QHBoxLayout()
        self.audio_player = QtMultimedia.QMediaPlayer(self)
        self.audio_output = QtMultimedia.QAudioOutput()
        self.audio_time_widget = AudioTimeWidget(self)
        self.listen_button = QtWidgets.QToolButton()
        self.pause_button = QtWidgets.QToolButton( )
        self.stop_button = QtWidgets.QToolButton()
        self.next_button = QtWidgets.QToolButton()
        self.volume_button = QtWidgets.QToolButton()
        self.previous_button = QtWidgets.QToolButton()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.audio_player.setAudioOutput(self.audio_output)

        self.main_v_layout.addLayout(self.buttons_h_layout)
        self.buttons_h_layout.addWidget(self.previous_button)
        self.buttons_h_layout.addWidget(self.listen_button)
        self.buttons_h_layout.addWidget(self.pause_button)
        self.buttons_h_layout.addWidget(self.stop_button)
        self.buttons_h_layout.addWidget(self.next_button)
        self.buttons_h_layout.addWidget(self.audio_time_widget)
        self.buttons_h_layout.addWidget(self.volume_button)

        self.listen_button.setIcon(get_pixmap('play'))
        self.pause_button.setIcon(get_pixmap('pause'))
        self.stop_button.setIcon(get_pixmap('stop'))
        self.next_button.setIcon(get_pixmap('next'))
        self.previous_button.setIcon(get_pixmap('previous'))
        self.volume_button.setIcon(get_pixmap('volume'))

        if self.parent.music_widget.table.rowCount() == 0:
            self.next_button.setEnabled(False)
            self.previous_button.setEnabled(False)
            self.listen_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.pause_button.setEnabled(False)

        self.previous_button.clicked.connect(self.previous_audio_button_click)
        self.listen_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        self.next_button.clicked.connect(self.next_audio_button_click)
        self.volume_button.clicked.connect(self.on_volume_button_click)
        self.audio_player.mediaStatusChanged.connect(self.on_media_status_changed)
    
    def on_media_status_changed(self, status: QtMultimedia.QMediaPlayer.MediaStatus):
        if status == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_audio_button_click()
    
    def change_volume_value(self) -> None:
        self.audio_output.setVolume(float(self.volume_dialog.volume_slider.value()) / 100)
    
    def on_volume_button_click(self) -> None:
        if self.volume_dialog:
            if self.volume_dialog.isVisible():
                self.volume_dialog.hide()
                return
        
        self.open_volume_dialog()

    def open_volume_dialog(self) -> None:
        if not self.volume_dialog:
            self.volume_dialog = VolumeSliderDialog(self, self.volume_button.mapToGlobal(QtCore.QPoint(-11, -72)))
            self.volume_dialog.volume_slider.setValue(self.audio_output.volume() * 100)
            self.volume_dialog.volume_slider.sliderReleased.connect(self.change_volume_value)
            return

        self.volume_dialog.show()

    def pause(self) -> None:
        self.audio_player.pause()

    def play(self) -> None:
        if not self.audio_player.hasAudio():
            self.set_audio(self.current_music_path)
            self.start_timers()

        if self.current_music_path != self.new_music_path:
            self.current_music_path = self.new_music_path
            self.stop_button.click()
            time.sleep(0.0008)
            self.set_audio(self.current_music_path)

        self.audio_player.play()
    
    def stop_calculate_timer(self) -> None:
        self.audio_time_widget.calculate_timer.stop()
    
    def stop_update_timer(self) -> None:
        self.audio_time_widget.update_timer.stop()

    def stop_timers(self) -> None:
        self.stop_calculate_timer()
        self.stop_update_timer()

    def start_timers(self) -> None:
        self.audio_time_widget.calculate_timer.start(500)
        self.audio_time_widget.update_timer.start(950)

    def switch_buttons(self, switch: bool) -> None:
        self.listen_button.setEnabled(switch)
        self.stop_button.setEnabled(switch)
        self.pause_button.setEnabled(switch)
        self.next_button.setEnabled(switch)
        self.previous_button.setEnabled(switch)  

    def next_audio_button_click(self) -> None:
        self.index_row = (self.parent.music_widget.table.currentRow() + 1) if self.index_row < self.parent.music_widget.table.rowCount() - 1 else 0
    
        self.parent.music_widget.table.setCurrentCell(self.index_row, 1)

        self.play()

    def previous_audio_button_click(self) -> None:
        self.index_row = (self.parent.music_widget.table.currentRow() - 1) if self.index_row > 0 else self.parent.music_widget.table.rowCount() - 1

        self.parent.music_widget.table.setCurrentCell(self.index_row, 1)

        self.play()

    def stop(self) -> None:
        self.audio_player.stop()

    def set_audio(self, music_path: str):
        self.audio_player.setSource(QtCore.QUrl().fromLocalFile(music_path))
        self.audio_metadata = self.audio_player.metaData()