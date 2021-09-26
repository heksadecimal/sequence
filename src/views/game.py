from backend.logic import Game
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from functools import partial


class Clickable_Label(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.create()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        return super().mousePressEvent(ev)





class Game_Renderer:
    def __init__(self, window) -> None:
        self.window = window
        self.game = Game()
        self.board = self.game.board

    def render(self) -> QWidget:

        self.mainPage = QWidget()

        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )

        # Main background image
        self.mainBG = QLabel(self.mainPage)

        self.mainBG.setPixmap(QPixmap("./img/main_bg.png"))

        self.mainBG.setScaledContents(True)

        self.mainBG.raise_()

        # Background Mask for darkening the image
        self.mainBM = QLabel(self.mainPage)

        self.mainBM.setStyleSheet("background-color: rgba(0, 0, 0, 120);")

        self.mainBM.raise_()

        x, y = 500, 0

        for row in self.board:
            for value in row:
                card = Clickable_Label(self.mainPage)

                card.setGeometry(QRect(x, y, 61, 90))

                card.setPixmap(QPixmap("img/cards/{}.png".format(value)))

                card.setScaledContents(True)

                card.setCursor(Qt.CursorShape.PointingHandCursor)

                card.clicked.connect(partial(self.click, card))

                x += 80

            x = 500

            y += 100

        return self.mainPage

    def click(self, card: QLabel):
        self.coin = QLabel(self.window)

        self.coin.setFixedSize(50, 50)

        self.coin.setScaledContents(True)

        self.coin.setStyleSheet("background-color: transparent")

        self.coin.setPixmap(QPixmap(self.game.getPlayerCoin()))

        self.coin.move(card.pos().x() + 5, card.pos().y() + 20)

        # opacity = QGraphicsOpacityEffect()

        # self.coin.setGraphicsEffect(opacity)

        self.coin.show()

        # self.animation = QPropertyAnimation(opacity , b"opacity")

        # self.animation.setStartValue(0)

        # self.animation.setEndValue(1)

        # self.animation.setDuration(400)

        # self.animation.finished.connect(self.coin.show)

        # self.animation.start()

    def responser(self, geometry):
        self.mainBG.setGeometry(geometry)

        self.mainBG.move(0, 0)

        self.mainBM.setGeometry(self.mainBG.geometry())
