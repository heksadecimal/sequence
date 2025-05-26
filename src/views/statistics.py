from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from functools import partial
from assets.animations import Animation
import views
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget
import configparser

config = configparser.ConfigParser()


class Statistics_Renderer:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.pieSlices = []
        self.updateDB()

    def updateDB(self):
        config.read("../sequence.ini")

        self.gamesWon = int(config.get("player", "gameswon"))
        self.gamesLost = int(config.get("player", "gameslost"))
        self.sequencemade = int(config.get("player", "sequencemade"))

    def render(self):
        self.updateDB()
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
        self.statsBG.setPixmap(QPixmap("../img/main_bg.png"))
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
        self.blackFrame.setStyleSheet("background-color: rgba(0, 0, 0, 120);")

        layout = QVBoxLayout()

        self.blackFrame.setLayout(layout)

        # Win
        self.layoutWin = QHBoxLayout()

        self.labelWin = QLabel()
        self.labelWin.setText("Games Won: ")
        self.labelWin.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.layoutWin.addWidget(self.labelWin, alignment=Qt.AlignmentFlag.AlignCenter)

        self.labelWinCount = QLabel()
        self.labelWinCount.setText(str(self.gamesWon))
        self.labelWinCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.layoutWin.addWidget(
            self.labelWinCount, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addLayout(self.layoutWin)

        self.lostLayout = QHBoxLayout()

        self.labelLost = QLabel()
        self.labelLost.setText("Games Lost: ")
        self.labelLost.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.lostLayout.addWidget(
            self.labelLost, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.labelWinCount = QLabel()
        self.labelWinCount.setText(str(self.gamesLost))
        self.labelWinCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.lostLayout.addWidget(
            self.labelWinCount, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addLayout(self.lostLayout)

        self.seqLayout = QHBoxLayout()

        self.seqLabel = QLabel()
        self.seqLabel.setText("Sequence Made: ")
        self.seqLabel.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.seqLayout.addWidget(self.seqLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.seqMade = QLabel()
        self.seqMade.setText(str(self.sequencemade))
        self.seqMade.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.seqLayout.addWidget(self.seqMade, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(self.seqLayout)

        self.pushButton = QPushButton(self.mainPage)
        self.pushButton.setGeometry(QRect(710, 670, 271, 61))
        self.pushButton.setFont(font)
        self.pushButton.setText("Back to Main Menu")
        self.pushButton.setStyleSheet(
            "color: #ebcb8b;\n" "background-color: rgb(125, 125, 125);"
        )

        self.pushButton.clicked.connect(
            lambda: self.window.setCentralWidget(
                views.menu.MenuRenderer(self.window).render()
            )
        )

        self.create_piechart()
        return self.mainPage

    def create_piechart(self):
        
        series = QPieSeries()

        font = QFont()
        font.setFamily("Comfortaa")
        font.setPixelSize(15)

        # Slice 1
        gameWon = series.append("Games Won", self.gamesWon)
        gameWon.setLabelFont(font)
        gameWon.clicked.connect(partial(self.startAnimation, gameWon))
        gameWon.setBrush(QBrush(QColor("#88C0D0")))
        gameWon.setLabelColor(QColor("#D8DEE9"))
        gameWon.setBorderColor(QColor("#2E3440"))
        gameWon.setExplodeDistanceFactor(0)
        self.pieSlices.append(gameWon)

        gameLost = series.append("Games Lost", self.gamesLost)
        gameLost.setLabelVisible(True)
        self.pieSlices.append(gameLost)
        gameLost.setLabelFont(font)
        gameLost.clicked.connect(partial(self.startAnimation, gameLost))
        gameLost.setLabelColor(QColor("#D8DEE9"))
        gameLost.setExploded(True)
        gameLost.setBrush(QBrush(QColor("#BF616A")))
        gameLost.setBorderColor(QColor("#2E3440"))
        gameLost.setExplodeDistanceFactor(0)

        seqCount = series.append("Sequence Created", self.sequencemade)
        seqCount.clicked.connect(partial(self.startAnimation, seqCount))
        seqCount.setExploded(True)
        seqCount.setLabelVisible(True)
        seqCount.setLabelFont(font)
        self.pieSlices.append(seqCount)
        seqCount.setLabelColor(QColor("#D8DEE9"))
        seqCount.setBrush(QBrush(QColor("#b48ead")))
        seqCount.setBorderColor(QColor("#2E3440"))
        seqCount.setExplodeDistanceFactor(0)

        # adding slice
        slice = QPieSlice()
        slice = series.slices()[0]
        slice.setExploded(True)
        slice.setLabelVisible(True)
        slice.setPen(QPen(QColor("#88c0d0"), 2))
        slice.setBrush(QColor("#88c0d0"))

        chart = QChart()

        chart.legend().hide()
        chart.addSeries(series)
        # chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.layout().setContentsMargins(0, 0, 0, 0)

        # chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chartview = QChartView(chart, self.mainPage)
        self.chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chartview.setBackgroundBrush(QColor(0, 0, 0, 0))
        self.chartview.chart().setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
        self.chartview.show()
        self.chartview.setStyleSheet("background-color: transparent")
        self.chartview.setGeometry(
            QRect(
                int(0.25 * self.mainPage.width()),
                int(0.1 * self.mainPage.height()),
                int(0.4 * self.mainPage.width()),
                400,
            )
        )

    def startAnimation(self, target: QPieSlice):
        self.animations = QParallelAnimationGroup()
        for slice in self.pieSlices:
            if slice != target and slice.explodeDistanceFactor() != 0:
                self.animations.addAnimation(
                    Animation.variantAnimation(
                        0.2, 0.0, 100, partial(self.parseFunc, slice)
                    )
                )

        self.animations.addAnimation(
            Animation.variantAnimation(
                0.0, 0.2, 100, lambda newVal: target.setExplodeDistanceFactor(newVal)
            )
        )

        self.animations.start()

    def parseFunc(self, target: QPieSlice, data):
        target.setExplodeDistanceFactor(data)

    def responser(self, geometry: QRect):
        self.statsBG.setGeometry(geometry)
        self.statsBG.move(QPoint(0, 0))

        self.label.setGeometry(self.statsBG.geometry())
        self.header.setGeometry(QRect(0, 70, self.label.width(), 50))

        self.blackFrame.setGeometry(
            QRect(
                int(0.3 * self.mainPage.width()),
                500,
                int(0.4 * self.mainPage.width()),
                400,
            )
        )

        self.chartview.setGeometry(
            QRect(
                int(0.3 * self.mainPage.width()),
                int(0.1 * self.mainPage.height()),
                int(0.4 * self.mainPage.width()),
                400,
            )
        )

        self.pushButton.setGeometry(QRect(int(0.25 * self.mainPage.width()), 910, 900, 61))
