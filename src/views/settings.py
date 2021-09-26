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

        self.label_3 = QLabel(self.mainPage)

        self.label_3.setGeometry(QRect(60, 50, 1121, 71))

        font = QFont()

        font.setPointSize(26)

        font.setBold(True)

        self.label_3.setFont(font)

        self.label_3.setStyleSheet(
            "color: rgb(220, 220, 0);\n" "background-color: rgb(125, 125, 125);"
        )

        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_4 = QLabel(self.mainPage)

        self.label_4.setGeometry(QRect(320, 250, 171, 51))

        font = QFont()

        font.setFamily("Comfortaa")

        font.setPointSize(14)

        font.setBold(True)

        font.setUnderline(False)

        self.label_4.setFont(font)

        self.label_4.setStyleSheet("color: rgb(220, 220, 0);")

        self.horizontalSlider = QSlider(self.mainPage)

        self.horizontalSlider.setGeometry(QRect(640, 250, 341, 31))

        self.horizontalSlider.setStyleSheet("")

        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.label_5 = QLabel(self.mainPage)

        self.label_5.setGeometry(QRect(1060, 960, 131, 51))

        self.label_6 = QLabel(self.mainPage)

        self.label_6.setGeometry(QRect(320, 340, 171, 51))

        font = QFont()

        font.setFamily("Comfortaa")

        font.setPointSize(14)

        font.setBold(True)

        font.setUnderline(False)

        self.label_6.setFont(font)

        self.label_6.setStyleSheet("color: rgb(220, 220, 0);")

        self.horizontalSlider_2 = QSlider(self.mainPage)

        self.horizontalSlider_2.setGeometry(QRect(640, 340, 341, 31))

        self.horizontalSlider_2.setOrientation(Qt.Orientation.Horizontal)

        self.label_133 = QLabel(self.mainPage)

        self.label_133.setGeometry(QRect(950, 960, 171, 51))

        font = QFont()

        font.setPointSize(14)

        font.setBold(True)

        font.setUnderline(False)

        self.label_133.setFont(font)

        self.label_133.setStyleSheet("color: rgb(220, 220, 0);")

        self.label_134 = QLabel(self.mainPage)

        self.label_134.setGeometry(QRect(320, 440, 171, 51))

        font = QFont()

        font.setFamily("Comfortaa")

        font.setPointSize(14)

        font.setBold(True)

        self.label_134.setFont(font)

        self.label_134.setStyleSheet("color: rgb(220, 220, 0);")

        self.comboBox = QComboBox(self.mainPage)

        self.comboBox.setGeometry(QRect(630, 440, 291, 51))

        font = QFont()

        font.setFamily("Comfortaa")

        font.setPointSize(14)

        font.setBold(True)

        self.comboBox.setFont(font)

        self.comboBox.setStyleSheet(
            "color: rgb(220, 220, 0);\n" "background-color: rgb(125, 125, 125);"
        )

        self.comboBox.addItem("")

        self.comboBox.addItem("")

        self.comboBox.addItem("")

        self.pushButton = QPushButton(self.mainPage)

        self.pushButton.setGeometry(QRect(510, 670, 271, 61))

        font = QFont()

        font.setFamily("Comfortaa")

        font.setPointSize(14)

        font.setBold(True)

        self.pushButton.setFont(font)

        self.pushButton.setStyleSheet(
            "color: rgb(220, 220, 0);\n" "background-color: rgb(125, 125, 125);"
        )

        self.animation.start()

        return self.mainPage

    def responser(self, geometry: QRect):
        self.settingsBG.setGeometry(geometry)

        self.settingsBG.move(QPoint(0, 0))

        self.settingsBM.setGeometry(self.settingsBG.geometry())
