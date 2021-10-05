from PyQt6.QtWidgets import (
    QGraphicsScene,
    QApplication,
    QGraphicsView,
    QGraphicsEllipseItem,
    QHBoxLayout,
)
import sys, random
from functools import partial
from assets.animations import Animation
from components.QLight import QLightReflectionButton

import views
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, QVariant, QVariantAnimation, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPixmap
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
        self.pieSlices = []

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

        self.layoutWin.addWidget(self.labelWin , alignment=Qt.AlignmentFlag.AlignCenter)

        self.labelWinCount = QLabel()
        self.labelWinCount.setText("0")
        self.labelWinCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.layoutWin.addWidget(self.labelWinCount , alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(self.layoutWin)

        self.lostLayout = QHBoxLayout()

        self.labelLost = QLabel()
        self.labelLost.setText("Games Lost: ")
        self.labelLost.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.lostLayout.addWidget(self.labelLost , alignment=Qt.AlignmentFlag.AlignCenter)

        self.labelWinCount = QLabel()
        self.labelWinCount.setText("0")
        self.labelWinCount.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.lostLayout.addWidget(self.labelWinCount , alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(self.lostLayout)

        self.seqLayout = QHBoxLayout()

        self.seqLabel = QLabel()
        self.seqLabel.setText("Sequence Made: ")
        self.seqLabel.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.seqLayout.addWidget(self.seqLabel , alignment=Qt.AlignmentFlag.AlignCenter)

        self.seqMade = QLabel()
        self.seqMade.setText("0")
        self.seqMade.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.seqLayout.addWidget(self.seqMade , alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(self.seqLayout)

        # self.labelWinRatio = QLabel(self.mainPage)
        # self.labelWinRatio.setText("Winning Ratio: ")
        # self.labelWinRatio.setGeometry(0.3 * self.mainPage.width(), 540, 350, 50)
        # self.labelWinRatio.setStyleSheet(
        #     "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        # )

        # self.labelWinRatioCount = QLabel(self.mainPage)
        # self.labelWinRatioCount.setText("0")
        # self.labelWinRatioCount.setGeometry(0.6 * self.mainPage.width(), 540, 350, 50)
        # self.labelWinRatioCount.setStyleSheet(
        #     "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        # )

        self.ratioLayout = QHBoxLayout()

        self.wRation = QLabel()
        self.wRation.setText("Winning Ratio: ")
        self.wRation.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.ratioLayout.addWidget(self.wRation , alignment=Qt.AlignmentFlag.AlignCenter)

        self.wRatioC = QLabel()
        self.wRatioC.setText("0")
        self.wRatioC.setStyleSheet(
            "background-color: transparent; font-size: 25px; font-family: Comfortaa; color: #ebcb8b"
        )

        self.ratioLayout.addWidget(self.wRatioC , alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(self.ratioLayout)
        
        self.pushButton = QLightReflectionButton(self.mainPage)
        self.pushButton.setFont(font)
        self.pushButton.setText("Back to Main Menu")
        self.pushButton.clicked.connect(
            lambda: self.window.setCentralWidget(
                views.profile.Profile_Renderer(self.window).render()
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
        slice = series.append("Games Won", 10)
        slice.setLabelFont(font)
        slice.clicked.connect(partial(self.startAnimation, slice))
        slice.setBrush(QBrush(QColor("#88C0D0")))
        slice.setLabelColor(QColor("#D8DEE9"))
        slice.setBorderColor(QColor("#2E3440"))
        slice.setExplodeDistanceFactor(0)
        self.pieSlices.append(slice)

        gWon = series.append("Games Lost", 20)
        gWon.setLabelVisible(True)
        self.pieSlices.append(gWon)
        gWon.setLabelFont(font)
        gWon.clicked.connect(partial(self.startAnimation, gWon))
        gWon.setLabelColor(QColor("#D8DEE9"))
        gWon.setExploded(True)
        gWon.setBrush(QBrush(QColor("#BF616A")))
        gWon.setBorderColor(QColor("#2E3440"))
        gWon.setExplodeDistanceFactor(0)

        gLose = series.append("Sequence Created", 10)
        gLose.clicked.connect(partial(self.startAnimation, gLose))
        gLose.setExploded(True)
        gLose.setLabelVisible(True)
        gLose.setLabelFont(font)
        self.pieSlices.append(gLose)
        gLose.setLabelColor(QColor("#D8DEE9"))
        gLose.setBrush(QBrush(QColor("#D08770")))
        gLose.setBorderColor(QColor("#2E3440"))
        gLose.setExplodeDistanceFactor(0)

        rGame = series.append("Game Ratio", 30)
        rGame.clicked.connect(partial(self.startAnimation, rGame))
        rGame.setExploded(True)
        rGame.setLabelFont(font)
        rGame.setLabelVisible(True)
        self.pieSlices.append(rGame)
        rGame.setLabelColor(QColor("#D8DEE9"))
        rGame.setBrush(QBrush(QColor("#A3BE8C")))
        rGame.setBorderColor(QColor("#2E3440"))
        rGame.setExplodeDistanceFactor(0)

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

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chartview = QChartView(chart, self.mainPage)
        self.chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chartview.setBackgroundBrush(QColor(0, 0, 0, 0))

        self.chartview.chart().setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))

        self.chartview.show()

        self.chartview.setStyleSheet("background-color: transparent")
        
        self.chartview.setGeometry(
            QRect(
                0.25 * self.mainPage.width(),
                .1 * self.mainPage.height(),
                0.4 * self.mainPage.width(),
                400,
            )
        )

    def startAnimation(self, target: QPieSlice):
        self.animations = QParallelAnimationGroup()
        for slice in self.pieSlices:
            if(slice != target and slice.explodeDistanceFactor() != 0):
                self.animations.addAnimation(Animation.variantAnimation(0.2 , 0.0 , 100 , partial(self.parseFunc , slice)))
        
        self.animations.addAnimation(Animation.variantAnimation(0.0 , 0.2 , 100 , lambda newVal: target.setExplodeDistanceFactor(newVal)))

        self.animations.start()

    def parseFunc(self , target: QPieSlice , data):
        target.setExplodeDistanceFactor(data)

    def responser(self, geometry: QRect):
        self.statsBG.setGeometry(geometry)
        self.statsBG.move(QPoint(0, 0))

        self.label.setGeometry(self.statsBG.geometry())
        self.header.setGeometry(QRect(0, 70, self.label.width(), 50))
        # self.labelWin.setGeometry(0.42 * self.mainPage.width(), 250, 350, 50)
        # self.labelLost.setGeometry(0.42 * self.mainPage.width(), 340, 350, 50)
        # self.labelSeqs.setGeometry(0.42 * self.mainPage.width(), 440, 350, 50)
        # self.labelWinRatio.setGeometry(0.42 * self.mainPage.width(), 540, 350, 50)
        # self.labelSeqsCount.setGeometry(0.6 * self.mainPage.width(), 440, 350, 50)
        # self.labelWinCount.setGeometry(0.6 * self.mainPage.width(), 250, 350, 50)
        # self.labelLostCount.setGeometry(0.6 * self.mainPage.width(), 340, 350, 50)
        # self.labelWinRatioCount.setGeometry(0.6 * self.mainPage.width(), 540, 350, 50)

        self.blackFrame.setGeometry(
            QRect(
                0.3 * self.mainPage.width(),
                500,
                0.4 * self.mainPage.width(),
                400,
            )
        )

        self.chartview.setGeometry(
            QRect(
                0.3 * self.mainPage.width(),
                .1 * self.mainPage.height(),
                0.4 * self.mainPage.width(),
                400,
            )
        )


        self.pushButton.setGeometry(QRect(0.25 * self.mainPage.width(), 910, 900, 61))
