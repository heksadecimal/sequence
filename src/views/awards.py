from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QWidget


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

        self.labelAward = QLabel(self.mainPage)

        self.labelAward.setGeometry(QRect(-10, 50, 1201, 71))

        self.labelAward.setText("Awards")

        font = QFont()

        font.setPointSize(36)

        font.setBold(True)

        self.labelAward.setFont(font)

        self.labelAward.setStyleSheet(
            "color: rgb(220, 220, 0);\n" "background-color: rgb(125, 125, 125);"
        )

        self.labelAward.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.labelAward.setObjectName("labelAward")

        self.frame_2 = QFrame(self.mainPage)

        self.frame_2.setGeometry(QRect(130, 210, 931, 751))

        self.frame_2.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        self.frame_2.setObjectName("frame_2")

        self.label_7 = QLabel(self.frame_2)

        self.label_7.setGeometry(QRect(70, 30, 91, 91))

        self.label_7.setStyleSheet("")

        self.label_7.setText("")

        self.label_7.setPixmap(QPixmap("../ui/../img/awards/chicken.png"))

        self.label_7.setScaledContents(True)

        self.label_7.setObjectName("label_7")

        return self.mainPage

    def responser(self, geometry):
        self.awardBG.setGeometry(geometry)

        self.awardBG.move(QPoint(0, 0))

        self.awardBM.setGeometry(self.awardBG.geometry())

        self.mainPage.setGeometry(
            QRect(0, 0, self.window.width(), self.window.height())
        )
