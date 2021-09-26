from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, QSize, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class Award_Renderer:
    def __init__(self, window) -> None:
        self.window = window

        self.animation = QParallelAnimationGroup()

    def render(self):
        self.mainPage = QWidget()

        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )

        self.awardBG = QLabel(self.mainPage)

        self.awardBG.setGeometry(QRect(0, 0, 1191, 1001))

        self.awardBG.setPixmap(QPixmap("../ui/../img/main_bg.png"))

        self.awardBG.setScaledContents(True)

        self.awardBM = QLabel(self.mainPage)

        self.awardBM.setGeometry(QRect(0, 0, 1191, 1061))

        self.awardBM.setStyleSheet("background-color: rgba(0, 0, 0, 120);")

        self.awardBM.setScaledContents(False)

        self.header = QLabel(self.mainPage)

        self.header.setGeometry(QRect(0, 70, self.window.width(), 50))

        self.header.setStyleSheet(
            "background-color: transparent; font-size: 56px; font-family: Comfortaa; color: #D8DEE9"
        )

        self.header.setText("Awards")

        self.header.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )

        awardsMap = [
            ["chicken", "milk", "two"],
            ["super_strength", "oops", "rising_star"],
            ["bulb", "grandmaster", "legend"],
        ]

        self.frame_2 = QFrame(self.mainPage)

        self.frame_2.setGeometry(QRect(130, 210, 931, 751))

        self.frame_2.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        layout = QVBoxLayout()

        self.frame_2.setLayout(layout)

        for row in awardsMap:
            hlayout = QHBoxLayout()

            for value in row:
                image = QLabel(self.frame_2)

                image.setPixmap(QPixmap("./img/awards/{}.png".format(value)))

                image.setFixedSize(QSize(100, 100))

                image.setScaledContents(True)

                hlayout.addWidget(image)

            layout.addLayout(hlayout)

        return self.mainPage

    def responser(self, geometry):
        self.awardBG.setGeometry(geometry)

        self.awardBG.move(QPoint(0, 0))

        self.awardBM.setGeometry(self.awardBG.geometry())

        self.mainPage.setGeometry(
            QRect(0, 0, self.window.width(), self.window.height())
        )
