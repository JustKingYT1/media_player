from typing import Optional
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
import src.settings
import pyaudio
import wave
import threading


class ToolsWidget(QtWidgets.QWidget):
    music_process: threading.Thread = None
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.is_paused: bool = False
        self.flag = False
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.listen_button = QtWidgets.QPushButton(text='Listen')
        self.stop_button = QtWidgets.QPushButton(text='Stop')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)

        self.main_h_layout.addWidget(self.listen_button)
        self.main_h_layout.addWidget(self.stop_button)

        self.listen_button.clicked.connect(self.on_listen_button_click)
        self.stop_button.clicked.connect(self.on_stop_button_click)

    def on_listen_button_click(self) -> None:
        if not self.flag:
            self.audio_thread = threading.Thread(target=self.start_play_audio)
            self.audio_thread.start()
        else:
            self.playback_audio()

    def on_stop_button_click(self) -> None:
        self.stop_audio()
    
    def playback_audio(self) -> None:
        if self.is_paused:
            self.is_paused = False
    
    def start_play_audio(self) -> None:
        self.flag = True

        chunk = 256

        format = 'wav'
        music_name = f'{src.settings.MUSIC_DIR}/{self.parent.music_widget.table.model().index(self.parent.music_widget.table.currentIndex().row(), 1).data()}.{format}'
        wf = wave.open(music_name, 'rb')

        # Создаем экземпляр PyAudio
        p = pyaudio.PyAudio()

        # Открываем поток для воспроизведения
        self.stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Читаем данные из аудиофайла и воспроизводим их по частям
        data = wf.readframes(chunk)
        while data:
            if not self.is_paused:
                self.stream.write(data)
                data = wf.readframes(chunk)
            else:
                self.stream.stop_stream()
                while self.is_paused:
                    pass
                self.stream.start_stream()

    def stop_audio(self) -> None:
        if not self.is_paused:
            self.is_paused = True

