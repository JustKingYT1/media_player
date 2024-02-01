from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
import src.settings
import pyaudio
import wave
import threading


class ToolsWidget(QtWidgets.QWidget):
    p = pyaudio.PyAudio()
    music_process: threading.Thread = None
    is_played: bool = False
    stop_flag: bool = False
    chunk_total = 0
    current_time = 0
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.is_paused: bool = False
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.listen_button = QtWidgets.QPushButton(text='Listen')
        self.stop_button = QtWidgets.QPushButton(text='Stop')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)

        self.main_h_layout.addWidget(self.listen_button)
        self.main_h_layout.addWidget(self.stop_button)

        self.stop_button.setEnabled(False)

        self.listen_button.clicked.connect(self.on_listen_button_click)
        self.stop_button.clicked.connect(self.on_stop_button_click)

    def start_new_thread_for_audio(self) -> None:
        self.audio_thread = threading.Thread(target=self.play_audio)
        self.audio_thread.start()
    
    def re_create_stream(self) -> None:
        self.stream, self.wf, self.data, _= self.create_stream()
        self.chunk_total = 0

    def on_listen_button_click(self) -> None:
        new_music_name = self.parent.music_widget.table.model().index(self.parent.music_widget.table.currentIndex().row(), 1).data()
        path_to_music = f'{src.settings.MUSIC_DIR}/{new_music_name}.wav'
        if not self.is_played:
            if not new_music_name:
                return
            self.is_paused = False
            self.stop_button.setEnabled(True)
            self.start_new_thread_for_audio()
            self.parent.audio_time_widget.timer.start(1000)
        else:
            if self.music_name != path_to_music and new_music_name:
                self.re_create_stream()
            else:
                self.playback_audio()

    def on_stop_button_click(self) -> None:
        self.stop_audio()
    
    def playback_audio(self) -> None:
        if self.is_paused:
            self.is_paused = False

    def create_stream(self):
        chunk = 256
        format = 'wav'
        self.music_name = f'{src.settings.MUSIC_DIR}/{self.parent.music_widget.table.model().index(self.parent.music_widget.table.currentIndex().row(), 1).data()}.{format}'
        wf = wave.open(self.music_name, 'rb')

        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(chunk)
        return stream, wf, data, chunk
    
    
    def play_audio(self) -> None:
        self.is_played = True

        self.stream, self.wf, self.data, chunk = self.create_stream()

        while self.data:
            if not self.is_paused and self.stream:
                self.stream.write(self.data)
                self.chunk_total += chunk
                self.current_time = self.chunk_total / float(self.wf.getframerate())
                self.data = self.wf.readframes(chunk)
            else:
                self.stream.stop_stream()
                while self.is_paused:
                    pass
                self.stream.start_stream()
        
    def stop_audio(self) -> None:
        if not self.is_paused:
            self.is_paused = True

