from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QTextEdit, QStackedWidget,
    QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont, QMovie, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")

current_dir = os.getcwd()
old_chat_message = ""

TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}\{Filename}"

def TempDirectoryPath(Filename):
    return rf"{TempDirPath}\{Filename}"

def SetMicrophoneStatus(command):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(TempDirectoryPath("Mic.data"), "w") as f:
        f.write(command)

def GetMicrophoneStatus():
    try:
        with open(TempDirectoryPath("Mic.data"), "r") as f:
            return f.read()
    except:
        return "False"

def SetAssistantStatus(Status):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(TempDirectoryPath("Status.data"), "w") as f:
        f.write(Status)

def GetAssistantStatus():
    try:
        with open(TempDirectoryPath("Status.data"), "r") as f:
            return f.read()
    except:
        return "Available..."

def ShowTextToScreen(Text):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(TempDirectoryPath("Responses.data"), "w", encoding="utf-8") as f:
        f.write(Text)

def AnswerModifier(text):
    lines = text.split('\n')
    return '\n'.join([i for i in lines if i.strip()])

def QueryModifier(query):
    return query.strip().lower()

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setFrameShape(QFrame.NoFrame)

        self.chat_text_edit.setStyleSheet("""
        QTextEdit{
            background:#0b0b0b;
            border:none;
            padding:15px;
            color:white;
        }
        """)

        layout.addWidget(self.chat_text_edit)

        self.gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('IGRIS.gif'))
        movie.setScaledSize(QSize(480,270))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()

        layout.addWidget(self.gif_label)

        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.start(500)

        self.setStyleSheet("background:#0b0b0b;")

    def loadMessages(self):
        global old_chat_message

        path = TempDirectoryPath('Responses.data')

        if not os.path.exists(path):
            return

        try:
            with open(path,"r",encoding="utf-8") as file:
                messages = file.read()

            if messages and messages != old_chat_message:
                self.chat_text_edit.append(messages)
                old_chat_message = messages
        except:
            pass

class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('IGRIS.gif'))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        self.mic_on = True

        self.mic_button = QPushButton()
        self.mic_button.setStyleSheet("background:transparent;border:none;")
        self.mic_button.clicked.connect(self.toggleMic)

        self.updateMicIcon()

        layout.addWidget(gif_label)
        layout.addWidget(self.mic_button, alignment=Qt.AlignCenter)

        self.setStyleSheet("background:#0b0b0b;")

    def updateMicIcon(self):
        if self.mic_on:
            pix = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
        else:
            pix = QPixmap(GraphicsDirectoryPath('Mic_off.png'))

        self.mic_button.setIcon(QIcon(pix))
        self.mic_button.setIconSize(QSize(60,60))

    def toggleMic(self):
        self.mic_on = not self.mic_on

        if self.mic_on:
            SetMicrophoneStatus("True")
        else:
            SetMicrophoneStatus("False")

        self.updateMicIcon()

class MessageScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(ChatSection())

        self.setStyleSheet("background:#0b0b0b;")

class CustomTopBar(QWidget):
    def __init__(self,parent,stacked_widget):
        super().__init__(parent)

        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20,0,20,0)

        title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet("color:white;font-size:16px;font-weight:bold;")

        home_button = QPushButton("Home")
        message_button = QPushButton("Chat")

        home_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))

        minimize_button = QPushButton("—")
        minimize_button.clicked.connect(parent.showMinimized)

        close_button = QPushButton("✕")
        close_button.clicked.connect(parent.close)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch()
        layout.addWidget(minimize_button)
        layout.addWidget(close_button)

        self.setStyleSheet("background:#0b0b0b;color:white;")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        stacked_widget = QStackedWidget()
        stacked_widget.addWidget(InitialScreen())
        stacked_widget.addWidget(MessageScreen())

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0,0,0,0)

        main_layout.addWidget(CustomTopBar(self,stacked_widget))
        main_layout.addWidget(stacked_widget)

        container.setStyleSheet("background:#0b0b0b;")
        self.setCentralWidget(container)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
