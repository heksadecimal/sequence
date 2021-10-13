from PyQt6.QtMultimedia import QSoundEffect
import views
from assets.animations import Animation
from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, QUrl, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QComboBox, QLabel, QPushButton, QSlider, QWidget
from backend.sound import play, changeVol


class Settings_Renderer:
    def __init__(self, window) -> None:
        self.window = window
        self.effect = QSoundEffect()
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
        self.animation.addAnimation(Animation.unfade( self.settingsBM, 300))

        # font
        font = QFont()
        font.setFamily("Comfortaa")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)

        # header
        self.header = QLabel(self.mainPage)
        self.header.setGeometry(QRect(0, 70, self.window.width(), 70))
        self.header.setStyleSheet(
            "background-color: transparent; font-size: 56px; font-family: Comfortaa; color: #ebcb8b"
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
        self.gameSound.setStyleSheet("color: #ebcb8b;background-color: transparent")

        # background game sound
        self.gameMusic = QLabel(self.mainPage)
        self.gameMusic.setText("Background Music")
        self.gameMusic.setGeometry(QRect(520, 340, 200, 61))
        self.gameMusic.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft
        )
        self.gameMusic.setStyleSheet("color: #ebcb8b;background-color: transparent")
        self.gameMusic.setFont(font)

        # seletion of bg music
        self.gameAudio = QLabel(self.mainPage)
        self.gameAudio.setText("Audio")
        self.gameAudio.setGeometry(QRect(520, 460, 200, 61))
        self.gameAudio.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft
        )
        self.gameAudio.setStyleSheet("color: #ebcb8b;background-color: transparent")
        self.gameAudio.setFont(font)

        # in-game sound slider
        self.gameSoundSlider = QSlider(self.mainPage)
        self.gameSoundSlider.setGeometry(QRect(920, 250, 300, 61))
        self.gameSoundSlider.setOrientation(Qt.Orientation.Horizontal)
        self.gameSoundSlider.setValue(100)
        self.gameSoundSlider.setStyleSheet(
            """
            QSlider{
                background-color: transparent
            }

            QSlider::handle{
                background-color: #ebcb8b;
                border-radius: 10px
            }
            """
        )
        self.gameSoundSlider.setFont(font)
        self.gameSoundSlider.valueChanged.connect(self.updateSound)


        # bg sound slider
        self.gameMusicSlider = QSlider(self.mainPage)
        self.gameMusicSlider.setGeometry(QRect(920, 340, 300, 61))
        self.gameMusicSlider.setValue(100)
        self.gameMusicSlider.setOrientation(Qt.Orientation.Horizontal)
        self.gameMusicSlider.setStyleSheet(
            "color: #ebcb8b;background-color: transparent"
        )
        self.gameMusicSlider.setStyleSheet(
            """
            QSlider{
                background-color: transparent
            }

            QSlider::handle{
                background-color: #ebcb8b;
                border-radius: 10px
            }
            """
        )
        # self.gameMusicSlider.setFont(font)
        #self.gameMusicSlider.valueChanged.connect(self.updateSound)

        # bg-audio selector
        self.comboBox = QComboBox(self.mainPage)
        self.comboBox.setGeometry(QRect(920, 440, 300, 61))
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet(
            "color: #ebcb8b;background-color: rgb(125, 125, 125);"
        )

        self.comboBox.addItem("casino1")
        self.comboBox.addItem("casino2")
        self.comboBox.addItem("casino3")
        self.comboBox.currentTextChanged.connect(self.updatePlayer)

        # back-button
        self.pushButton = QPushButton(self.mainPage)
        self.pushButton.setGeometry(QRect(710, 670, 271, 61))
        self.pushButton.setFont(font)
        self.pushButton.setText("Back to Main Menu")
        self.pushButton.setStyleSheet(
            "color: #ebcb8b;\n" "background-color: rgb(125, 125, 125);"
        )

        self.pushButton.clicked.connect(
            lambda: self.window.setCentralWidget(
                views.profile.Profile_Renderer(self.window).render()
            )
        )

        self.animation.start()

        return self.mainPage

    def updatePlayer(self, event):
        volume = self.gameSoundSlider.value() / 100
        song = self.comboBox.currentText()
        play(song, volume)
        
    def updateSound(self, event):
        changeVol(self.gameSoundSlider.value())


    def responser(self, geometry: QRect):
        self.settingsBG.setGeometry(geometry)
        self.settingsBG.move(QPoint(0, 0))
        self.settingsBM.setGeometry(self.settingsBG.geometry())
        self.header.setGeometry(QRect(0, 70, self.window.width(), 100))
        self.gameSound.setGeometry(QRect(0.35 * self.settingsBG.width(), 250, 200, 61))
        self.gameMusic.setGeometry(QRect(0.35 * self.settingsBG.width(), 340, 200, 61))
        self.gameAudio.setGeometry(QRect(0.35 * self.settingsBG.width(), 460, 200, 61))
        self.gameSoundSlider.setGeometry(
            QRect(0.6 * self.settingsBG.width(), 250, 0.1 * self.settingsBG.width(), 20)
        )

        self.gameMusicSlider.setGeometry(
            QRect(0.6 * self.settingsBG.width(), 340, 0.1 * self.settingsBG.width(), 20)
        )

        self.comboBox.setGeometry(
            QRect(0.6 * self.settingsBG.width(), 440, 0.1 * self.settingsBG.width(), 61)
        )

        self.pushButton.setGeometry(QRect(0.43 * self.settingsBG.width(), 670, 271, 61))
