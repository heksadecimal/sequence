import views
from assets.charts import QBarChart
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QFont, QPen, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)


class Statistics_Renderer:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window

    def render(self):
        self.mainPage = QWidget()
        self.mainPage.setGeometry(0, 0, self.window.width(), self.window.height())
        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )

        # font
        font = QFont()
        font.setFamily("Comfortaa")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)

        self.statsBG = QLabel(self.mainPage)
        self.statsBG.setGeometry(QRect(0, 0, 1191, 1001))
        self.statsBG.setPixmap(QPixmap("./img/main_bg.png"))
        self.statsBG.setScaledContents(True)

        self.label = QLabel(self.mainPage)
        self.label.setGeometry(
            QRect(0, 0, self.mainPage.width(), self.statsBG.height())
        )
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 170);")

        self.header = QLabel(self.mainPage)
        self.header.setGeometry(QRect(0, 70, self.label.width(), 50))
        self.header.setText("Statistics")
        self.header.setStyleSheet(
            "background-color: transparent; font-size: 56px; font-family: Comfortaa; color: #ebcb8b"
        )
        self.header.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )

        self.blackFrame = QLabel(self.mainPage)
        self.blackFrame.setGeometry(
            QRect(
                0.25 * self.mainPage.width(),
                240,
                0.4 * self.mainPage.width(),
                400,
            )
        )
        self.blackFrame.setStyleSheet("background-color: rgba(0, 0, 0, 120);")

        self.labelWin = QLabel(self.mainPage)
        self.labelWin.setText("Games Won: ")
        self.labelWin.setGeometry(0.3 * self.mainPage.width(), 250, 350, 50)
        self.labelWin.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.labelWinCount = QLabel(self.mainPage)
        self.labelWinCount.setText("0")
        self.labelWinCount.setGeometry(0.6 * self.mainPage.width(), 250, 350, 50)
        self.labelWinCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.labelLost = QLabel(self.mainPage)
        self.labelLost.setText("Games Lost: ")
        self.labelLost.setGeometry(0.3 * self.mainPage.width(), 340, 350, 50)
        self.labelLost.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.labelLostCount = QLabel(self.mainPage)
        self.labelLostCount.setText("0")
        self.labelLostCount.setGeometry(0.6 * self.mainPage.width(), 340, 350, 50)
        self.labelLostCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.labelSeqs = QLabel(self.mainPage)
        self.labelSeqs.setText("Sequences Made: ")
        self.labelSeqs.setGeometry(0.3 * self.mainPage.width(), 440, 350, 50)
        self.labelSeqs.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.labelSeqsCount = QLabel(self.mainPage)
        self.labelSeqsCount.setText("0")
        self.labelSeqsCount.setGeometry(0.6 * self.mainPage.width(), 440, 350, 50)
        self.labelSeqsCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.labelWinRatio = QLabel(self.mainPage)
        self.labelWinRatio.setText("Winning Ratio: ")
        self.labelWinRatio.setGeometry(0.3 * self.mainPage.width(), 540, 350, 50)
        self.labelWinRatio.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.labelWinRatioCount = QLabel(self.mainPage)
        self.labelWinRatioCount.setText("0")
        self.labelWinRatioCount.setGeometry(0.6 * self.mainPage.width(), 540, 350, 50)
        self.labelWinRatioCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        # back-button
        self.pushButton = QPushButton(self.mainPage)
        self.pushButton.setGeometry(QRect(710, 670, 271, 61))
        self.pushButton.setFont(font)
        self.pushButton.setText("Back to Main Menu")
        self.pushButton.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: rgb(125, 125, 125);"
        )
        self.pushButton.clicked.connect(
            lambda: self.window.setCentralWidget(
                views.profile.Profile_Renderer(self.window).render()
            )
        )

        return self.mainPage

    def responser(self, geometry: QRect):
        self.statsBG.setGeometry(geometry)
        self.statsBG.move(QPoint(0, 0))

        self.label.setGeometry(self.statsBG.geometry())
        self.header.setGeometry(QRect(0, 70, self.label.width(), 50))
        self.labelWin.setGeometry(0.3 * self.mainPage.width(), 250, 350, 50)
        self.labelLost.setGeometry(0.3 * self.mainPage.width(), 340, 350, 50)
        self.labelSeqs.setGeometry(0.3 * self.mainPage.width(), 440, 350, 50)
        self.labelWinRatio.setGeometry(0.3 * self.mainPage.width(), 540, 350, 50)
        self.pushButton.setGeometry(QRect(0.37 * self.mainPage.width(), 670, 271, 61))
