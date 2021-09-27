from assets.animations import Animation
from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QComboBox, QLabel, QPushButton, QSlider, QWidget


class Settings_Renderer:
    def __init__(self, window) -> None:
        self.window = window

        self.animation = QParallelAnimationGroup()

    def render(self):
        self.mainPage = QWidget()
        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )


        # Main Background
        self.settingsBG = QLabel(self.mainPage)
        self.settingsBG.setPixmap(QPixmap("../img/main_bg.png"))
        self.settingsBG.setScaledContents(True)


        # Mask
        self.settingsBM = QLabel(self.mainPage)
        self.settingsBM.setStyleSheet("background-color: rgba(0, 0, 0, 170);")
        self.animation.addAnimation(Animation.unfade(Animation, self.settingsBM))


        # font
        font = QFont()
        font = QFont()
        font.setFamily("Comfortaa")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)


        # header
        self.header = QLabel(self.mainPage)
        self.header.setGeometry(QRect(0, 70, self.window.width(), 70))
        self.header.setStyleSheet(
            "background-color: #ebcb8b; font-size: 56px; font-family: Comfortaa; color: #88C0D0"
        )
        self.header.setText("Settings")
        self.header.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )


        # in-game sound
        self.gameSound = QLabel(self.mainPage)
        self.gameSound.setGeometry(QRect(520, 250, 200, 61))
        self.gameSound.setText("In-Game Sound")
        self.gameSound.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft
        )
        self.gameSound.setFont(font)
        self.gameSound.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: transparent"
        )


        # background game sound
        self.gameMusic = QLabel(self.mainPage)
        self.gameMusic.setText("Background Music")
        self.gameMusic.setGeometry(QRect(520, 340, 200, 61))
        self.gameMusic.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft
        )
        self.gameMusic.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: transparent"
        )
        self.gameMusic.setFont(font)


        # seletion of bg music
        self.gameAudio = QLabel(self.mainPage)
        self.gameAudio.setText("Audio")
        self.gameAudio.setGeometry(QRect(520, 440, 200, 61))
        self.gameAudio.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft
        )
        self.gameAudio.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: transparent"
        )
        self.gameAudio.setFont(font)


        # in-game sound slider
        self.gameSoundSlider = QSlider(self.mainPage)
        self.gameSoundSlider.setGeometry(QRect(920, 250, 300, 61))
        self.gameSoundSlider.setStyleSheet(
            "color: rgb(255, 255, 255);background-color: transparent"
        )
        self.gameSoundSlider.setOrientation(Qt.Orientation.Horizontal)

        # bg sound slider
        self.gameMusicSlider = QSlider(self.mainPage)
        self.gameMusicSlider.setGeometry(QRect(920, 340, 300, 61))
        self.gameMusicSlider.setOrientation(Qt.Orientation.Horizontal)
        self.gameMusicSlider.setStyleSheet(
            "color: rgb(255, 255, 255);background-color: transparent"
        )


        # bg-audio selector
        self.comboBox = QComboBox(self.mainPage)
        self.comboBox.setGeometry(QRect(920, 440, 300, 61))
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: rgb(125, 125, 125);"
        )
        self.comboBox.addItem("casino 1")
        self.comboBox.addItem("casino 2")
        self.comboBox.addItem("casino 3")
        

        #back-button
        self.pushButton = QPushButton(self.mainPage)
        self.pushButton.setGeometry(QRect(710, 670, 271, 61))
        self.pushButton.setFont(font)
        self.pushButton.setText("Back to Main Menu")
        self.pushButton.setStyleSheet(
            "color: rgb(220, 220, 0);\n" "background-color: rgb(125, 125, 125);"
        )
        self.animation.start()

        return self.mainPage

    def responser(self, geometry: QRect):
        self.settingsBG.setGeometry(geometry)
        self.settingsBG.move(QPoint(0, 0))
        self.settingsBM.setGeometry(self.settingsBG.geometry())
        self.header.setGeometry(QRect(0, 70, self.window.width(), 100))


