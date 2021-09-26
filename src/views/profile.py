from assets.widgets import QButton
from assets.animations import Animation
from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, Qt
from PyQt6.QtGui import QCursor, QFont, QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class Profile_Renderer:
    def __init__(self, window: QWidget) -> None:
        self.window = window

        self.animation = QParallelAnimationGroup()

    def render(self) -> QWidget:
        # Create main page
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

        # self.animation.addAnimation(Animation.unfade(Animation , self.mainBM))

        # Logo
        self.lableLogo = QLabel(self.mainPage)

        self.lableLogo.setGeometry(QRect(500, 80, 181, 151))

        self.lableLogo.setPixmap(QPixmap("../img/logo.png"))

        self.lableLogo.setScaledContents(True)

        self.lableLogo.raise_()

        # self.animation.addAnimation(Animation.unfade(Animation , self.lableLogo))

        self.buttons = QLabel(self.mainPage)

        self.buttons.setGeometry(0, 0, 650, 500)

        self.buttons.show()

        self.layout = QVBoxLayout()

        for push_button_text in ["Profile", "New Game", "Load Saved Games", "Exit"]:
            widget = QButton(None)

            widget.setFixedSize(600, 70)

            widget.setText(push_button_text)

            self.layout.addWidget(widget)

        self.buttons.setLayout(self.layout)

        self.animation.start()

        return self.mainPage

    def responser(self, geometry: QRect):
        self.mainBG.setGeometry(geometry)

        self.mainBG.move(QPoint(0, 0))

        self.mainBM.setGeometry(self.mainBG.geometry())

        # Move the label logo
        x = 0.5 * (geometry.width() - 181)

        y = 0.17 * (geometry.height() - 151)

        self.lableLogo.setGeometry(QRect(x, y, 181, 151))

        # The buttons
        x = 0.38 * (geometry.width() - 181)

        y = 0.4 * (geometry.height() - 151)

        self.buttons.move(x, y)
