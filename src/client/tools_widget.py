from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
import src.settings
import pyaudio
import wave
import threading
import enum
import time

class ModifyBool(enum.Enum):
    Truth = 2
    SemiTruth = 1
    NoTruth = 0


class ToolsWidget(QtWidgets.QWidget):
    p = pyaudio.PyAudio()
    is_played: ModifyBool = ModifyBool.NoTruth
    stop_flag: bool = False
    chunk_total = 0
    current_time = 0
    index_row = -1
    chunk = 256
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.is_paused: bool = False
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.buttons_h_layout = QtWidgets.QHBoxLayout()
        self.timer = QtCore.QTimer(self)
        self.listen_button = QtWidgets.QPushButton(text='Listen')
        self.next_button = QtWidgets.QPushButton('Next')
        self.previous_button = QtWidgets.QPushButton('Previous')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.main_v_layout.addLayout(self.buttons_h_layout)
        self.buttons_h_layout.addWidget(self.previous_button)
        self.buttons_h_layout.addWidget(self.listen_button)
        self.buttons_h_layout.addWidget(self.next_button)

        self.next_button.setEnabled(False)
        self.previous_button.setEnabled(False)

        self.timer.timeout.connect(self.update_frame)

        self.previous_button.clicked.connect(self.previous_audio_button_click)
        self.listen_button.clicked.connect(self.on_listen_button_click)
        self.next_button.clicked.connect(self.next_audio_button_click)

    def calculate_current_time(self) -> None:
        self.chunk_total += self.chunk
        self.current_time = int(self.chunk_total / float(self.wf.getframerate()))

    def update_frame(self) -> None:
        new_music_name, _ = self.get_music_name()
        path_to_music = f'{src.settings.MUSIC_DIR}/{new_music_name}.wav'
        if self.music_path != path_to_music and new_music_name:
            self.listen_button.setText('Listen')
            self.is_played = ModifyBool.SemiTruth
        
    def get_music_name(self, switch=0, index=0, flag=False) -> str:
        new_music_path = self.parent.music_widget.table.model().index((self.parent.music_widget.table.currentIndex().row() + switch) if not flag else (index + switch), 1).data()
        return new_music_path, (self.index_row + switch)

    def on_listen_button_click(self) -> None:
        new_music_name, _ = self.get_music_name()
        path_to_music = f'{src.settings.MUSIC_DIR}/{new_music_name}.wav'
        match self.is_played:
            case ModifyBool.NoTruth:
                if not new_music_name:
                    return
                self.is_played = ModifyBool.Truth
                self.is_paused = False
                self.index_row = self.parent.music_widget.table.currentIndex().row()
                self.start_new_thread_for_audio()
                self.start_timers()
                self.timer.start(500)
                self.listen_button.setText('Pause')
                self.next_button.setEnabled(True)
                self.previous_button.setEnabled(True)

            case ModifyBool.SemiTruth:
                self.is_played = ModifyBool.Truth
                self.listen_button.setText('Pause')
                
                if self.music_path != path_to_music and new_music_name:
                    self.re_create_stream(flag=False)
                else:
                    self.playback_audio()

            case ModifyBool.Truth:
                self.is_played = ModifyBool.SemiTruth
                self.stop_audio()
                self.listen_button.setText('Listen')

    def stop_timers(self) -> None:
        self.parent.audio_time_widget.calculate_timer.stop()
        self.parent.audio_time_widget.update_timer.stop()

    def start_timers(self) -> None:
        self.parent.audio_time_widget.calculate_timer.start(1000)
        self.parent.audio_time_widget.update_timer.start(1000)

    def stop_audio(self) -> None:
        if not self.is_paused:
            self.is_paused = True
        
        self.stop_timers()

    def playback_audio(self) -> None:
        if self.is_paused:
            self.is_paused = False
        
        self.start_timers()

    def next_audio_button_click(self) -> None:
        self.music_name, self.index_row = self.get_music_name(switch=1, index=self.index_row, flag=True)
        if self.music_name:
            self.parent.music_widget.table.setCurrentCell(self.index_row, 1)
            self.re_create_stream(True)
        else:
            self.music_name, self.index_row = self.get_music_name(switch=-self.index_row, index=self.index_row, flag=True)
            self.parent.music_widget.table.setCurrentCell(self.index_row, 1)
            self.re_create_stream(True)

    def previous_audio_button_click(self) -> None:
        self.music_name, self.index_row = self.get_music_name(switch=-1, index=self.index_row, flag=True)
        if self.music_name:
            self.parent.music_widget.table.setCurrentCell(self.index_row, 1)
            self.re_create_stream(True)
        else:
            self.music_name, self.index_row = self.get_music_name(switch=self.parent.music_widget.table.rowCount(), index=self.index_row, flag=True)
            self.parent.music_widget.table.setCurrentCell(self.index_row, 1)
            self.re_create_stream(True)

    def re_create_stream(self, flag) -> None:
        self.stream, self.wf, self.data= self.create_stream(flag)
        self.chunk_total = 0

    def create_stream(self, flag=False):
        format = 'wav'
        if not flag:
            self.music_name, _ = self.get_music_name()
        self.music_path = f'{src.settings.MUSIC_DIR}/{self.music_name}.{format}'
        wf = wave.open(self.music_path, 'rb')

        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(self.chunk)
        return stream, wf, data
    
    def play_audio(self) -> None:
        self.is_played = ModifyBool.Truth

        self.stream, self.wf, self.data = self.create_stream()

        while self.data:
            if not self.is_paused and self.stream:
                self.stream.write(self.data)
                self.data = self.wf.readframes(self.chunk)
                self.calculate_current_time()
            else:
                self.stream.stop_stream()
                while self.is_paused:
                    pass
                self.stream.start_stream()
        
        self.chunk_total = 0
        self.is_played = ModifyBool.NoTruth
        
    def start_new_thread_for_audio(self) -> None:
        self.audio_thread = threading.Thread(target=self.play_audio)
        self.audio_thread.start()