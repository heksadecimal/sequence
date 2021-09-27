from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, QSize, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class Award_Renderer:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window

        self.animation = QParallelAnimationGroup()

    def render(self):
        self.mainPage = QWidget()

        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )

        self.awardBG = QLabel(self.mainPage)

        self.awardBG.setGeometry(QRect(0, 0, 1191, 1001))

        self.awardBG.setPixmap(QPixmap("./img/main_bg.png"))

        self.awardBG.setScaledContents(True)

        self.awardBM = QLabel(self.mainPage)

        self.awardBM.setGeometry(QRect(0, 0, 1191, 1001))

        self.awardBM.setStyleSheet("background-color: rgba(0, 0, 0, 200);")

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
            ["super", "oops", "rising_star"],
            ["bulb", "master", "legend"],
        ]

        self.awardsLayoutParent = QLabel(self.mainPage)

        self.awardsLayoutParent.setGeometry(
            QRect(0, 90, self.window.width(), self.window.height() - 100)
        )

        self.awardsLayoutParent.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout()

        self.awardsLayoutParent.setLayout(layout)

        for row in awardsMap:
            hlayout = QHBoxLayout()

            for value in row:
                l = QVBoxLayout()

                image = QLabel()

                image.setPixmap(QPixmap("./img/awards/{}.png".format(value)))
                image.setFixedSize(QSize(100, 100))

                image.setScaledContents(True)

                image.setAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter
                )

                l.addWidget(image)
                # l.setGeometry(imageGeometry)

                name = QLabel()

                name.setFixedHeight(50)

                name.setFixedWidth(130)

                name.setStyleSheet(
                    "color: #D8DEE9; font-size: 20px; font-family: Comfortaa; text-transform: uppercase;border-size: 5px"
                )

                name.setText(value.replace("_", " "))

                name.setAlignment(
                    Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignBottom
                )

                l.addWidget(name)

                hlayout.addLayout(l)

            layout.addLayout(hlayout)

        return self.mainPage

    def responser(self, geometry):
        self.awardBG.setGeometry(geometry)

        self.awardBG.move(QPoint(0, 0))

        self.awardBM.setGeometry(self.awardBG.geometry())

        self.mainPage.setGeometry(
            QRect(0, 0, self.window.width(), self.window.height())
        )

        self.header.setGeometry(QRect(0, 70, self.window.width(), 50))

        self.awardsLayoutParent.setGeometry(
            QRect(0, 90, self.window.width(), self.window.height() - 90)
        )
