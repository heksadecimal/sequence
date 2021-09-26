from PyQt6.QtCore import QObject, QParallelAnimationGroup, QPoint, QPropertyAnimation, QRect, QThread, pyqtSignal
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget
from time import sleep
from functools import partial
from sys import setrecursionlimit
from threading import Thread

setrecursionlimit(100000)

time = 100

width = 1000

def run(time , width , target):
    # pixelFill = width / time

    # size = target.size()

    # size.setWidth(size.width() + pixelFill)

    # width -= pixelFill

    # time -= 1

    # print(pixelFill)

    # target.setFixedSize(size)
    while time > 0:
        pixelFill = width / time

        size = target.size()

        size.setWidth(size.width() + pixelFill)

        width -= pixelFill

        time -= 1

        sleep(0.01)

        target.setFixedSize(size)


class QBarChart(QLabel):
    def __init__(self , window: QWidget):
        super().__init__(window)

        self.entryValues = []

        self.setGeometry(QRect(10 , 300 , 1980 , 1080))

        self.cX , self.cY = 0 , 10

    def addInEntry(self , name , value):
        self.entryValues.append(value)

        bar = QLabel(self)

        bar.setGeometry(self.cX , self.cY , 50 , 70)

        self.cX += 200

        bar.setStyleSheet("background-color: #CDEBFF")

        opacity = QGraphicsOpacityEffect()

        opacity.setOpacity(0.7)

        bar.setGraphicsEffect(opacity)

        bar.show()

        self.show()

        # self.animation = QParallelAnimationGroup()

        # animation = QPropertyAnimation(bar , b"geometry")

        # animation.setStartValue(QRect(self.cX , self.cY , 0 , 60))

        # animation.setEndValue(QRect(self.cX , self.cY , 1000 , 60))

        # animation.setDuration(700)

        # self.animation.addAnimation(animation)
        
        # self.animation.start()\
        thread = Thread(target=run , args=(time , width , bar))

        thread.setDaemon(True)

        thread.start()