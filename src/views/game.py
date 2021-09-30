import views
from collections import defaultdict
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
    QDialog,
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
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.create()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        return super().mousePressEvent(ev)


class Game_Renderer:
    def __init__(self, window) -> None:
        self.window = window
        # self.window.closeEvent = self.cleanClose


        self.game = Game()
        self.animation = QParallelAnimationGroup()
        self.board = self.game.board
        self.bot = player(self.showCards)
        self.challenger = player(self.showCards)
        self.position = defaultdict(lambda: (0, 0))
        self.revposition = defaultdict(QRect)
        self.game.distribute(self.bot)
        self.game.distribute(self.challenger)
        self.coins = defaultdict(Clickable_Label)
        print("1: ", self.bot.playerCards)
        print("2: ", self.challenger.playerCards)
        print("---------------------")

    def saveAndClose(self):
        print("HEYYEYEY")
        self.window.setCentralWidget(
                views.profile.Profile_Renderer(self.window).render()
        )

    def cleanClose(self):
        self.ok = QDialog(self.mainPage)
        self.ok.setWindowTitle("Quit Sequece")
        self.ok.setGeometry(
            0.4 * self.window.geometry().width(),
            0.4 * self.window.geometry().height(),
            500,
            200,
        )
        self.ok.setStyleSheet("background-color: #3b4252")

        self.quitLabel = QLabel(self.ok)
        self.quitLabel.setGeometry(
            self.quitLabel.geometry().x() + 100,
            self.quitLabel.geometry().y() + 10,
            300,
            100,
        )
        self.quitLabel.setText("Do you wish to save you game ?")
        self.quitLabel.setStyleSheet(
            "color: #ebcb8b; font-size: 18px; font-style: comfortaa"
        )

        self.yes = QPushButton(self.ok)
        self.yes.setText("YES")
        self.yes.setGeometry(
            self.yes.geometry().x() + 100,
            self.yes.geometry().y() + 120,
            self.yes.geometry().width(),
            self.yes.geometry().height(),
        )
        self.yes.show()

        self.no = QPushButton(self.ok)
        self.no.setText("NO")
        self.no.setGeometry(
            self.no.geometry().x() + 250,
            self.no.geometry().y() + 120,
            self.no.geometry().width(),
            self.no.geometry().height(),
        )
        self.no.show()
        self.no.clicked.connect(lambda : self.window.setCentralWidget(
                views.profile.Profile_Renderer(self.window).render()
        ))
        self.yes.clicked.connect(lambda : self.saveAndClose())
        
        self.quitLabel.show()
        self.ok.exec()

 
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


        # back-button
        self.backPushButton = QPushButton(self.mainPage)
        self.backPushButton.setGeometry(.04 * self.mainPage.width(), .12 * self.mainPage.height(), 120, 90)
        self.backPushButton.setText("Go Back")
        self.backPushButton.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: rgb(125, 125, 125);font-style: comfortaa;font-size: 20px"
        )
        self.backPushButton.clicked.connect(lambda: self.cleanClose())

        self.currentCards = QLabel(self.mainPage)
        self.currentCards.setStyleSheet("background-color: transparent")
        self.currentCardsLayout = QHBoxLayout()
        self.currentCards.setLayout(self.currentCardsLayout)
        self.currentCards.show()

        constX = 0.31 * self.window.width()

        x, y = constX, 10

        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
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

                self.position[QRect(x, y, 50, 70)] = (i, j)
                self.revposition[(i, j)] = QRect(x, y, 50, 70)

                x += 70

            x = constX
            y += 80

        self.animation.start()

        self.showCards()

        return self.mainPage

    def placeCoin(self, position: QRect, image):
        print(position)
        self.coin = Clickable_Label(self.window)
        self.coin.setFixedSize(40, 40)
        self.coin.setScaledContents(True)
        self.coin.setStyleSheet("background-color: transparent")
        self.coin.setPixmap(QPixmap(f"../img/coins/{image}.png"))
        self.coin.move(position.x() + 5, position.y() + 15)
        self.coin.clicked.connect(partial(self.click, self.coin))
        self.coins[position] = self.coin
        self.coin.show()

    def click(self, card: QLabel):

        x, y = self.position[card.geometry()]
        ok = self.game.setBox(self.challenger, self.bot.playerBox, x, y)
        if not ok:
            return

        if ok == 2:
            self.coins[card.geometry()].hide()
        else:
            self.placeCoin(self.revposition[(x, y)], "one")
            self.challenger.addCard(self.game.getNewCard())

        while True:
            ok = self.game.makeRandomMove(self.bot, self.challenger)
            if not ok:
                continue

            i, j, x = ok
            pos = self.revposition[(i, j)]
            if not x:
                self.coins[card.geometry()].hide()
            else:
                self.placeCoin(pos, "two")
            break

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
        self.currentCards.setGeometry(
            QRect(
                0.27 * self.window.width(),
                0.85 * self.window.height(),
                0.45 * self.window.width(),
                0.1 * self.window.height(),
            )
        )

    def showCards(self):
        self.currentCards.hide()

        self.currentCards = QLabel(self.mainPage)
        self.currentCards.setStyleSheet("background-color: #ebcb8b")
        self.currentCards.setGeometry(
            QRect(
                0.27 * self.window.width(),
                0.85 * self.window.height(),
                0.45 * self.window.width(),
                0.1 * self.window.height(),
            )
        )

        self.currentCards.show()

        self.newLayout = QHBoxLayout()

        self.currentCards.setLayout(self.newLayout)

        for cardTag in self.challenger.playerCards:
            card = QLabel()

            card.setScaledContents(True)

            card.setFixedSize(50, 70)

            card.setPixmap(QPixmap("./img/cards/{}.png".format(cardTag)))

            self.newLayout.addWidget(card)
