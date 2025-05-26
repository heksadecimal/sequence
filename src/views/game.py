from backend.sound import playIG
from components.QLight import QLightReflectionButton
import views
import configparser
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
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
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
        self.game = Game()
        self.config = configparser.ConfigParser()
        self.config.read("../sequence.ini")
        self.animation = QParallelAnimationGroup()
        self.board = self.game.board
        self.savedBoard = {}
        self.bot = player("bot")
        self.challenger = player("challenger")
        self.position = defaultdict(lambda: (0, 0))
        self.revposition = defaultdict(QWidget)
        self.game.distribute(self.bot)
        self.game.distribute(self.challenger)
        # self.challenger.playerCards = ["JC"] * 5

        self.coins = defaultdict(Clickable_Label)

    def cleanClose(self):
        self.ok = QDialog(self.mainPage)
        self.ok.setWindowTitle("Quit Sequece")
        self.ok.setFixedSize(500, 250)
        self.ok.setStyleSheet("background-color: #3b4252")

        self.label = QLabel(self.ok)
        self.label.setFixedSize(self.ok.size())

        layout = QVBoxLayout()

        self.quitLabel = QLabel()
        self.quitLabel.setText("Do you wish to leave in midst of the game ?")
        self.quitLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        self.quitLabel.setStyleSheet(
            "color: #ebcb8b; font-size: 18px; font-style: comfortaa"
        )

        layout.addWidget(self.quitLabel)

        self.no = QLightReflectionButton()
        self.no.setFixedHeight(50)
        self.no.setText("no")
        self.no.clicked.connect(lambda: self.ok.close())

        layout.addWidget(self.no)

        self.yes = QLightReflectionButton()
        self.yes.setText("YES")
        self.yes.setFixedHeight(50)
        self.yes.clicked.connect(
            lambda: self.window.setCentralWidget(
                views.menu.MenuRenderer(self.window).render()
            )
        )

        layout.addWidget(self.yes)

        self.label.setLayout(layout)

        self.ok.exec()

    def render(self) -> QWidget:
        self.mainPage = QWidget()
        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )

        # Main background image
        self.mainBG = QLabel(self.mainPage)
        self.mainBG.setPixmap(QPixmap("../img/main_bg.png"))
        self.mainBG.setScaledContents(True)
        self.mainBG.raise_()

        # Background Mask for darkening the image
        self.mainBM = QLabel(self.mainPage)
        self.mainBM.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        self.mainBM.raise_()

        # back-button
        self.menuPushButton = QPushButton(self.mainPage)
        self.menuPushButton.setGeometry(
            int(0.04 * self.mainPage.width()), int(0.12 * self.mainPage.height()), 120, 90
        )
        self.menuPushButton.setText("Go Back")
        self.menuPushButton.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: rgb(125, 125, 125);font-style: comfortaa;font-size: 20px"
        )
        self.menuPushButton.clicked.connect(lambda: self.cleanClose())

        self.currentCards = QLabel(self.mainPage)
        self.currentCards.setStyleSheet("background-color: transparent")
        self.currentCardsLayout = QHBoxLayout()
        self.currentCards.setLayout(self.currentCardsLayout)
        self.currentCards.show()

        constX = int(0.31 * self.window.width())

        x, y = constX, 10

        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                card = Clickable_Label(self.mainPage)
                card.setGeometry(QRect(500, 10, 50, 70))
                card.setPixmap(QPixmap("../img/cards/{}.png".format(value)))
                card.setScaledContents(True)
                card.setCursor(Qt.CursorShape.PointingHandCursor)
                card.setProperty("codeName", value)
                card.clicked.connect(partial(self.click, card))

                animation = QPropertyAnimation(card, b"pos")
                animation.setStartValue(QPoint(500, 0))
                animation.setEndValue(QPoint(x, y))
                animation.setDuration(300)
                self.animation.addAnimation(animation)

                if value in self.savedBoard:
                    print(self.savedBoard[value])
                    if self.savedBoard[value] == "bot":
                        self.click(card, [x, y], True, "two")
                    else:
                        self.click(card, [int(x), int(y)], True, "one")

                self.position[QRect(x, y, 50, 70)] = (i, j)
                # self.revposition[(i, j)] = QRect(x, y, 50, 70)
                self.revposition[(i, j)] = card

                x += 70

            x = constX
            y += 80

        self.animation.start()

        self.showCards()

        return self.mainPage

    def placeCoin(self, position: QRect, image, card: QWidget, who="challenger"):
        # if(who != None):
        # self.coinPos[card.property("codeName")] = who

        self.coin = Clickable_Label(self.mainPage)
        self.coin.setFixedSize(40, 40)
        self.coin.setScaledContents(True)
        self.coin.setStyleSheet("background-color: transparent")
        self.coin.setPixmap(QPixmap(f"../img/coins/{image}.png"))
        self.coin.move(position.x() + 5, position.y() + 15)
        self.coin.clicked.connect(partial(self.click, card))
        self.coins[position] = self.coin
        self.coin.show()
        

    def updateAwards(self):
        awards = set()
        if self.gamesLost >= 5:
            awards.add("oops")

        if self.gamesWon:
            awards.add("milk")

        if self.sequenceMade:
            awards.add("chicken")

        if self.gamesWon > 1:
            awards.add("two")

        if self.continousWin == 5:
            awards.add("rising_star")

        if self.gamesWon + self.gamesLost >= 50:
            awards.add("bulb")

        if self.gamesWon >= 50:
            awards.add("master")

        if self.gamesWon >= 100:
            awards.add("legend")
            
        if len(awards) >= 4:
            awards.add("super")

        return ", ".join(list(awards))

    def updateUserData(self, score):
        self.gamesWon = int(self.config.get("player", "gamesWon"))
        self.sequenceMade = int(self.config.get("player", "sequenceMade"))
        self.gamesLost = int(self.config.get("player", "gamesLost"))
        self.continousWin = int(self.config.get("player", "continousWin"))

        if score:
            self.gamesWon += 1
            self.sequenceMade += 1
            self.continousWin += 1
            self.config.set("player", "gamesWon", str(self.gamesWon))
            self.config.set("player", "sequenceMade", str(self.sequenceMade))
        else:
            self.gamesLost += 1
            self.continousWin = 0
            self.config.set("player", "gamesLost", str(self.gamesLost + 1))

        self.config.set(
            "player",
            "gamesPlayed",
            str(int(self.config.get("player", "gamesPlayed")) + 1),
        )

        awards = self.updateAwards()
        self.config.set("player", "awards", awards)

        with open("../sequence.ini", "w") as c:
            self.config.write(c)

    def declare(self, status, who=""):
        flash = QDialog(self.mainPage)
        message = QLabel(flash)
        flash.setGeometry(
            int(0.35 * self.mainPage.width()), int(0.4 * self.mainPage.height()), 700, 300
        )
        flash.setStyleSheet("background-color: #3b4252")

        message = QLabel(flash)
        message.setGeometry(
            message.geometry().x() + 100,
            message.geometry().y() + 10,
            550,
            100,
        )
        message.setStyleSheet("color: #ebcb8b; font-size: 18px; font-style: comfortaa")
        pushButtonMenu = QPushButton(flash)
        pushButtonMenu.setText("Return to Main Menu")
        pushButtonMenu.setGeometry(
            pushButtonMenu.geometry().x() + 250,
            pushButtonMenu.geometry().y() + 200,
            pushButtonMenu.geometry().width() + 50,
            pushButtonMenu.geometry().height(),
        )
        pushButtonMenu.clicked.connect(
            lambda: self.window.setCentralWidget(
                views.menu.MenuRenderer(self.window).render()
            )
        )

        if status == 1:
            if who == "challenger":
                playIG("gameWin")
                message.setText(
                    "Wohoo! That was a great match and you won. Congrats !!!!!"
                )
                self.updateUserData(1)
            else:
                playIG("gameLose")
                message.setText("Oops! You were close. Better Luck newxt time ;_;")
                self.updateUserData(0)
        else:
            message.setText("WoW that was close. Looks like you need a rematch :)")

        flash.show()

    def click(self, card: QLabel, position=None, f=False, image=None):

        x, y = self.position[card.geometry()]

        ok = self.game.setBox(self.challenger, self.bot.playerBox, x, y)

        if not ok:
            return

        playIG("coinPlace")
        if ok == 2:
            self.coins[card.geometry()].hide()
        else:
            self.placeCoin(self.revposition[(x, y)].geometry(), "one", card)
            self.challenger.addCard(self.game.getNewCard())

        if self.game.winner:
            self.declare(1, "challenger")
            return

        if not self.game.deck:
            self.declare(0)
            return

        while True:
            ok = self.game.makeRandomMove(self.bot, self.challenger)
            if not ok:
                continue

            i, j, x = ok
            pos = self.revposition[(i, j)].geometry()
            if not x:
                self.coins[card.geometry()].hide()
            else:
                self.placeCoin(pos, "two", self.revposition[(i, j)], "bot")
            break

        if self.game.winner:
            self.declare(1)
            return

        if not self.game.deck:
            self.declare(1)
            self.declare(0)
            return

        self.showCards()
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
                int(0.27 * self.window.width()),
                int(0.85 * self.window.height()),
                int(0.45 * self.window.width()),
                int(0.1 * self.window.height()),
            )
        )

    def showCards(self):
        self.currentCards.hide()

        self.currentCards = QLabel(self.mainPage)
        self.currentCards.setStyleSheet("background-color: #ebcb8b")
        self.currentCards.setGeometry(
            QRect(
                int(0.27 * self.window.width()),
                int(0.85 * self.window.height()),
                int(0.45 * self.window.width()),
                int(0.1 * self.window.height()),
            )
        )

        self.newLayout = QHBoxLayout()
        self.currentCards.show()
        self.currentCards.setLayout(self.newLayout)


        for cardTag in self.challenger.playerCards:
            card = QLabel()
            card.setScaledContents(True)
            card.setFixedSize(50, 70)
            card.setPixmap(QPixmap("../img/cards/{}.png".format(cardTag)))

            self.newLayout.addWidget(card)

    # def saveGame(self):
    #     self.label.move(QPoint(-510, 0))

    #     self.newLabel = QLabel(self.ok)
    #     self.newLabel.setFixedSize(self.ok.size())
    #     self.newLabel.move(510, 0)

    #     layout = QVBoxLayout()

    #     label = QLabel(text="Enter the name for the game")
    #     label.setStyleSheet("color: #D8DEE9; font-size: 20px; font-family: Comfortaa")
    #     label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)

    #     layout.addWidget(label)

    #     textInput = QLineEdit()
    #     textInput.setFixedHeight(50)

    #     textInput.setStyleSheet(
    #         """
    #     QLineEdit{
    #         color: #D8DEE9;
    #         font-size: 20px;
    #         font-family: Comfortaa;
    #     }

    #     QLineEdit:focus{
    #         border: 1px solid #2E3440
    #     }
    #     """
    #     )

    #     layout.addWidget(textInput)
    #     layout.setContentsMargins(20, 0, 20, 10)

    #     button = QLightReflectionButton()
    #     button.setText("Save Game")
    #     button.setFixedHeight(50)
    #     button.clicked.connect(partial(self.saveAndClose, textInput))

    #     layout.addWidget(button)
    #     layout.setSpacing(20)

    #     self.newLabel.setLayout(layout)

    #     self.label.stackUnder(self.newLabel)

    #     self.newLabel.show()

    #     # Animations

    #     self.animation = QParallelAnimationGroup()
    #     self.animation.addAnimation(Animation.fade(self.label, 500))
    #     self.animation.addAnimation(
    #         Animation.moveAnimation(self.label, QPoint(-510, 0), 500)
    #     )
    #     self.animation.addAnimation(Animation.unfade(self.newLabel, 500))
    #     self.animation.addAnimation(
    #         Animation.moveAnimation(self.newLabel, QPoint(0, 0), 500)
    #     )
    #     self.animation.start()

