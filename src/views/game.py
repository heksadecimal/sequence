from collections import defaultdict
import enum
from backend.logic import Game
from backend.player import player
from PyQt6.QtCore import (
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRect,
    Qt,
    pyqtSignal,
)
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
        self.animation = QParallelAnimationGroup()
        self.board = self.game.board
        self.chance = 1
        self.bot = player(self.showCards)
        self.challenger = player(self.showCards)
        self.position = defaultdict()
        self.game.distribute(self.bot)
        self.game.distribute(self.challenger)
        print("1: ", self.bot.playerCards)
        print("2: ", self.challenger.playerCards)
        print("---------------------")

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

        self.currentCards = QLabel(self.mainPage)
        self.currentCards.setStyleSheet("background-color: transparent")
        self.currentCardsLayout = QHBoxLayout()
        self.currentCards.setLayout(self.currentCardsLayout)
        self.currentCards.show()

        constX = .25 * self.window.width()

        x, y = constX , 10

        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                card = Clickable_Label(self.mainPage)
                card.setGeometry(QRect(500, 10, 50, 70))
                card.setPixmap(QPixmap("img/cards/{}.png".format(value)))
                card.setScaledContents(True)
                card.setCursor(Qt.CursorShape.PointingHandCursor)
                card.clicked.connect(partial(self.click, card))

                animation = QPropertyAnimation(card, b"pos")
                animation.setStartValue(QPoint(500, 0))
                animation.setEndValue(QPoint(x, y))
                animation.setDuration(300)
                self.animation.addAnimation(animation)

                self.position[card.geometry] = (i,j)

                x += 70

            x = constX
            y += 80

        self.animation.start()

        self.showCards()

        return self.mainPage

    def click(self, card: QLabel):

        x , y = self.position[card.geometry]
        p1, p2 = self.bot, self.challenger
        if self.chance % 2 == 0:
            p1, p2 = p2 , p1

        ok = self.game.setBox(p1, p2.playerBox, x, y)
        if not ok:
            return
        
        self.coin = Clickable_Label(self.window)
        self.coin.setFixedSize(40, 40)
        self.coin.setScaledContents(True)
        self.coin.setStyleSheet("background-color: transparent")
        playerCoin = "one" if self.chance % 2 else "two"
        if ok == 2:
            playerCoin = "null"
            
        self.coin.setPixmap(QPixmap(f"../img/coins/{playerCoin}.png"))
        self.coin.move(card.pos().x() + 5, card.pos().y() + 15)
        self.chance += 1
        p1.addCard(self.game.getNewCard())

        self.showCards()

        print("1: ", self.bot.playerCards)
        print("2: ", self.challenger.playerCards)
        print("---------------------")
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
        self.currentCards.setGeometry(QRect(0.2 * self.window.width() , 0.85 * self.window.height() , .45 * self.window.width() , 0.1 * self.window.height() ))


    def showCards(self):
        self.currentCards.hide()

        self.currentCards = QLabel(self.mainPage)

        self.currentCards.setStyleSheet("background-color: yellow")

        self.currentCards.setGeometry(QRect(0.2 * self.window.width() , 0.85 * self.window.height() , .45 * self.window.width() , 0.1 * self.window.height() ))

        self.currentCards.show()

        self.newLayout = QHBoxLayout()

        self.currentCards.setLayout(self.newLayout)

        for cardTag in self.bot.playerCards:
            card = QLabel()

            card.setScaledContents(True)

            card.setFixedSize(50 , 70)

            card.setPixmap(QPixmap("./img/cards/{}.png".format(cardTag)))

            self.newLayout.addWidget(card)

