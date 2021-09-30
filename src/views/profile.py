from views.settings import Settings_Renderer
from views.awards import Award_Renderer
from views.game import Game_Renderer
from views.statistics import Statistics_Renderer
from assets.widgets import QButton
from assets.animations import Animation
from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, Qt, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QFont,
    QImage,
    QMouseEvent,
    QPainter,
    QPixmap,
    QWindow,
)
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def mask_image(imageData, imgtype="png", size=64):

    image = QImage.fromData(imageData, imgtype)
    image.convertToFormat(QImage.Format.Format_ARGB32)

    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )

    image = image.copy(rect)

    out_img = QImage(imgsize, imgsize, QImage.Format.Format_ARGB32)
    out_img.fill(QColor(0, 0, 0, 0))

    brush = QBrush(image)

    painter = QPainter(out_img)
    painter.setBrush(brush)

    painter.setPen(Qt.PenStyle.NoPen)

    painter.drawEllipse(0, 0, imgsize, imgsize)

    painter.end()
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(
        size,
        size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )

    return pm

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

class Profile_Renderer:
    def __init__(self, window: QMainWindow) -> None:
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
        self.animation.addAnimation(Animation.unfade(Animation, self.mainBM))

        # Profile Picture
        self.lableLogo = QLabel(self.mainPage)
        self.lableLogo.setStyleSheet("background-color: transparent")
        self.lableLogo.setGeometry(QRect(500, 80, 181, 151))
        self.lableLogo.setPixmap(QPixmap("../img/logo.png"))
        self.lableLogo.setScaledContents(True)
        self.lableLogo.raise_()

        # Logo
        file = QFileDialog(self.mainPage)
        self.cat = Clickable_Label(self.mainPage)
        self.cat.setStyleSheet("border-radius: 50%;background-color: transparent")
        self.cat.setGeometry(QRect(1500, 80, 90, 90))
        self.img = open("../img/cat.png", "rb").read()
        self.cat.setPixmap(mask_image(self.img))
        self.cat.setScaledContents(True)
        self.cat.clicked.connect(self.updatePicture)
        self.cat.raise_()

        # fade animation
        self.animation.addAnimation(Animation.unfade(Animation, self.lableLogo))
        self.buttons = QLabel(self.mainPage)
        self.buttons.setGeometry(0, 0, 650, 500)
        self.buttons.setStyleSheet("background-color: transparent")
        self.buttons.show()

        # menu layout
        self.layout = QVBoxLayout()
        buttons = [
            ["Profile", self.openStats],
            ["New Game", self.newGame],
            ["Load Saved Games", self.loadSaves],
            ["Awards", self.openAwards],
            [
                "Settings",
                self.openSettings,
            ],
            ["Exit", self.quit],
        ]

        for text, func in buttons:
            widget = QButton(None)

            widget.setFixedSize(600, 70)
            widget.clicked.connect(func)
            widget.setText(text)
            self.layout.addWidget(widget)

        self.buttons.setLayout(self.layout)
        self.animation.start()
        return self.mainPage

    def responser(self, geometry: QRect):
        self.mainBG.setGeometry(geometry)
        self.mainBG.move(QPoint(0, 0))
        self.mainBM.setGeometry(self.mainBG.geometry())
        self.cat.setGeometry(QRect(0.9 * self.mainPage.width(), 80, 90, 90))

        # Move the label logo
        x = 0.5 * (geometry.width() - 181)
        y = 0.17 * (geometry.height() - 151)
        self.lableLogo.setGeometry(QRect(x, y, 181, 151))

        # The buttons
        x = 0.38 * (geometry.width() - 181)
        y = 0.4 * (geometry.height() - 151)
        self.buttons.move(x, y)

    def openStats(self):
        def second():
            self.window.setCentralWidget(Statistics_Renderer(self.window).render())
            self.animation = Animation.unfade(Animation, self.window.centralWidget())
            self.animation.start()

        self.animation = Animation.fade(Animation, self.window.centralWidget())
        self.animation.finished.connect(second)
        self.animation.start()

    def newGame(self):
        def second():
            self.window.setCentralWidget(Game_Renderer(self.window).render())

            self.animation = Animation.unfade(Animation, self.window.centralWidget())
            self.animation.start()

        self.animation = Animation.fade(Animation, self.window.centralWidget())
        self.animation.finished.connect(second)
        self.animation.start()

    def loadSaves(self):
        pass

    def openAwards(self):
        def second():
            self.window.setCentralWidget(Award_Renderer(self.window).render())

            self.animation = Animation.unfade(Animation, self.window.centralWidget())
            self.animation.start()

        self.animation = Animation.fade(Animation, self.window.centralWidget())
        self.animation.finished.connect(second)
        self.animation.start()

    def openSettings(self):
        def second():
            self.window.setCentralWidget(Settings_Renderer(self.window).render())

            self.animation = Animation.unfade(Animation, self.window.centralWidget())
            self.animation.start()

        self.animation = Animation.fade(Animation, self.window.centralWidget())
        self.animation.finished.connect(second)
        self.animation.start()

    def quit(self):
        quitDialog = QDialog(self.window)
        quitDialog.setWindowTitle("You sure you wanna quit?")
        quitDialog.set
        quitDialog.show()

    def updatePicture(self):
        self.fDialog = QFileDialog()

        imagePath, *args = self.fDialog.getOpenFileName(self.mainPage, 'choose picture', '.')
        # imagePath = str(imagePath)
        with open(imagePath, 'rb') as image:
            newImage = mask_image(image.read(), imgtype=imagePath[imagePath.rindex('.') + 1:])
            self.cat.setPixmap(newImage)