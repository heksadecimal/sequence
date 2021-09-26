from assets.charts import QBarChart
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QFont, QPen, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

class Statistics_Renderer:
    def __init__(self, window) -> None:
        self.window = window

    def render(self):
        self.mainPage = QWidget()

        self.profileBG = QLabel(self.mainPage)

        self.profileBG.setGeometry(QRect(0, 0, 1191, 1001))

        self.profileBG.setText("")

        self.profileBG.setPixmap(QPixmap("../ui/../img/main_bg.png"))

        self.profileBG.setScaledContents(True)

        self.label = QLabel(self.mainPage)

        self.label.setGeometry(QRect(0, 0, 1191, 1001))

        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 120);")

        self.label_2 = QLabel(self.mainPage)

        self.label_2.setGeometry(QRect(60, 50, 1121, 71))

        font = QFont()

        font.setPointSize(26)

        font.setBold(True)

        self.label_2.setFont(font)

        self.label_2.setStyleSheet(
            "color: rgb(220, 220, 0);\n" "background-color: rgb(125, 125, 125);"
        )

        self.label_2.setText("Statistics")

        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        chart = QBarChart(self.mainPage)

        chart.addInEntry("Apple" , 0)

        # chart.addInEntry("Apple" , 0)

        # chart.addInEntry("Apple" , 0)

        return self.mainPage
