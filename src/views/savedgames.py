from configparser import ConfigParser
from functools import partial
from PyQt6.QtCore import QParallelAnimationGroup, QRect, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget
from assets.animations import Animation
from components.RoundJollyButtons import Rounded_Jolly_Button
from json import loads

from views.game import Clickable_Label, Game_Renderer

class Saved_Games:
    def __init__(self , window: QMainWindow):
        self.window = window

    def render(self) -> QWidget:
        self.mainPage = QWidget()

        # Main background image
        self.mainBG = QLabel(self.mainPage)
        self.mainBG.setPixmap(QPixmap("../img/main_bg.png"))
        self.mainBG.setScaledContents(True)
        self.mainBG.raise_()

        # Background Mask for darkening the image
        self.mainBM = QLabel(self.mainPage)
        self.mainBM.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        self.mainBM.raise_()
        self.animation = Animation.unfade(self.mainBM , 300)

        self.animation.start()

        self.mainPage.resizeEvent = self.responser

        self.header = QLabel(text="Your Saved Games" , parent=self.mainPage)

        self.header.setStyleSheet("""color: #EBCB8B; font-size: 50px; font-family: Comfortaa; background-color: transparent""")

        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)

        self.config = ConfigParser()

        self.config.read("../sequence.ini")

        item = loads(self.config.get("games" , "gameDic"))

        self.games = QLabel(self.mainPage)

        self.games.setContentsMargins(0 , 0 , 0 , 0)

        self.games.setStyleSheet("background-color: orange; padding: 0px")

        layout = QHBoxLayout()
        
        layout.setContentsMargins(0 , 0 , 0 , 0)

        for name , board in item.items():
            layout.addWidget(self.createNewCard(name , partial(self.openSaveGame , board)))
        
        self.games.setLayout(layout)

        return self.mainPage

    def responser(self , event):
        geometry = self.mainPage.geometry()

        self.animations = QParallelAnimationGroup()

        self.animations.addAnimation(Animation.variantAnimation(self.header.geometry() , QRect(0 , 50 , geometry.width() , 70) , 300 , lambda newValue: self.header.setGeometry(newValue)))

        self.animations.addAnimation(Animation.variantAnimation(self.mainBG.geometry() , QRect(0 , 0 , geometry.width() , geometry.height()) , 300 , lambda newValue: self.mainBG.setGeometry(newValue)))

        self.animations.addAnimation(Animation.variantAnimation(self.mainBM.geometry() , QRect(0 , 0 , geometry.width() , geometry.height()) , 300 , lambda newValue: self.mainBM.setGeometry(newValue)))

        self.animations.addAnimation(Animation.variantAnimation(self.games.geometry() , QRect(200 , 200 , geometry.width() - 400 , 50) , 300 , lambda newValue: self.games.setGeometry(newValue)))

        self.animations.start()

    def createNewCard(self , details , callback) -> QWidget:
        self.card = QLabel()

        self.card.setFixedHeight(50)

        self.card.setStyleSheet("background-color: #2E3440")

        layout = QHBoxLayout()

        layout.setContentsMargins(20 , 0 , 20 , 0)

        label = Clickable_Label()

        label.setText(details)

        label.setStyleSheet("color: #D8DEE9; font-size: 20px; font-family: Comfortaa")
        
        layout.addWidget(label)

        button = Rounded_Jolly_Button(None , "./img/delete.svg")

        layout.addWidget(button , alignment=Qt.AlignmentFlag.AlignVCenter)

        label.clicked.connect(callback)

        self.card.setLayout(layout)

        return self.card

    def openSaveGame(self , board):
        def second():
            gameRenderer = Game_Renderer(self.window)

            gameRenderer.setBoard(board)

            self.window.setCentralWidget(gameRenderer.render())

            self.animation = Animation.unfade(self.window.centralWidget() , 300)

            self.animation.start()

        self.animation = Animation.fade(self.window.centralWidget() , 300)
        self.animation.finished.connect(second)
        self.animation.start()