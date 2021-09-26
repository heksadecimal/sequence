from assets.charts import QBarChart
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QFont, QPen, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QMainWindow, QVBoxLayout, QWidget


class Statistics_Renderer:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window

    def render(self):
        self.mainPage = QWidget()

        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )

        self.profileBG = QLabel(self.mainPage)

        self.profileBG.setGeometry(QRect(0, 0, 1191, 1001))

        self.profileBG.setPixmap(QPixmap("./img/main_bg.png"))

        self.profileBG.setScaledContents(True)

        self.label = QLabel(self.mainPage)

        self.label.setGeometry(QRect(0, 0, 1191, 1001))

        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 120);")

        self.header = QLabel(self.mainPage)

        self.header.setGeometry(QRect(0, 70, self.window.width(), 50))

        self.header.setStyleSheet(
            "background-color: transparent; font-size: 56px; font-family: Comfortaa; color: #88C0D0"
        )

        self.header.setText("Statistics")

        self.header.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )

        return self.mainPage

    def responser(self, geometry: QRect):
        self.profileBG.setGeometry(geometry)

        self.profileBG.move(QPoint(0, 0))

        self.label.setGeometry(self.profileBG.geometry())
