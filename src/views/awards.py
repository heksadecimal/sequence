import configparser
import views
from PyQt6.QtCore import QParallelAnimationGroup, QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPixmap
from PyQt6.QtWidgets import (
    QDialog,
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


class Award_Renderer:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.animation = QParallelAnimationGroup()

    def render(self):
        self.mainPage = QWidget()

        self.mainPage.resizeEvent = lambda event: self.responser(
            self.mainPage.geometry()
        )

        config = configparser.ConfigParser()
        config.read("../sequence.ini")
        awards = config.get("player", "awards").split(", ")

        self.awardBG = QLabel(self.mainPage)
        self.awardBG.setGeometry(QRect(0, 0, 1191, 1001))
        self.awardBG.setPixmap(QPixmap("../img/main_bg.png"))
        self.awardBG.setScaledContents(True)

        self.awardBM = QLabel(self.mainPage)
        self.awardBM.setGeometry(QRect(0, 0, 1191, 1001))
        self.awardBM.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
        self.awardBM.setScaledContents(False)

        self.header = QLabel(self.mainPage)
        self.header.setGeometry(QRect(0, 70, self.window.width(), 50))
        self.header.setStyleSheet(
            "background-color: transparent; font-size: 56px; font-family: Comfortaa; color: #ebcb8b"
        )
        self.header.setText("Awards")
        self.header.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )

        self.menuPushButton = QPushButton(self.mainPage)
        self.menuPushButton.setGeometry(50, 50, 90, 90)
        self.menuPushButton.setText("Go Back")
        self.menuPushButton.setStyleSheet(
            "color: rgb(220, 220, 0);background-color: rgb(125, 125, 125);font-size:20px"
        )
        self.menuPushButton.clicked.connect(
            lambda: self.window.setCentralWidget(
                views.menu.MenuRenderer(self.window).render()
            )
        )

        awardsMap = [
            ["chicken", "milk", "two"],
            ["super", "oops", "rising_star"],
            ["bulb", "master", "legend"],
        ]

        self.awardsLayoutParent = QLabel(self.mainPage)
        self.awardsLayoutParent.setGeometry(
            QRect(0, 90, self.window.width(), self.window.height() - 100)
        )
        self.awardsLayoutParent.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout()
        self.awardsLayoutParent.setLayout(layout)

        awardData = {
            "chicken": {
                "needed": 1,
                "info": "Create A Sequence",
                "won": False,
                "when": "-",
            },
            "milk": {"needed": 1, "info": "Win A Game", "won": False, "when": "-"},
            "two": {"needed": 2, "info": "Win Two Game", "won": False, "when": "-"},
            "super": {"needed": 4, "info": "Win 4 Awards", "won": False, "when": "-"},
            "oops": {"needed": 5, "info": "Lose 5 Games", "won": False, "when": "-"},
            "rising_star": {
                "needed": 5,
                "info": "Win 5 Games in a row",
                "won": False,
                "when": "-",
            },
            "bulb": {"needed": 5, "info": "Play 50 matches", "won": False, "when": "-"},
            "master": {
                "needed": 50,
                "info": "Win 50 Matches",
                "won": False,
                "when": "-",
            },
            "legend": {
                "needed": 100,
                "info": "Win 100 Games",
                "won": False,
                "when": "-",
            },
        }

        for row in awardsMap:
            hlayout = QHBoxLayout()

            for value in row:
                l = QVBoxLayout()

                image = Clickable_Label()
                image.setPixmap(QPixmap("../img/awards/{}.png".format(value)))
                image.setFixedSize(QSize(100, 100))
                image.setScaledContents(True)
                image.setAlignment(
                    Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
                )
                image.clicked.connect(
                    partial(
                        self.showData,
                        awardData[value],
                        QPixmap("../img/awards/{}.png".format(value)),
                    )
                )

                if value in awards:
                    claim = QLabel(image)
                    stamp = QPixmap("../img/stamp.png")
                    claim.setPixmap(stamp)
                    claim.setScaledContents(True)
                    claim.setAlignment(
                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
                    )
                    claim.setGeometry(image.geometry())
                    claim.show()

                l.addWidget(image)

                name = QLabel()
                name.setFixedHeight(50)
                name.setFixedWidth(130)
                name.setStyleSheet(
                    "color: #D8DEE9; font-size: 20px; font-family: Comfortaa; text-transform: uppercase;"
                )
                name.setText(value.replace("_", " "))
                name.setAlignment(
                    Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
                )

                l.addWidget(name)

                hlayout.addLayout(l)

            layout.addLayout(hlayout)

        return self.mainPage

    def responser(self, geometry):
        self.awardBG.setGeometry(geometry)
        self.awardBG.move(QPoint(0, 0))
        self.awardBM.setGeometry(self.awardBG.geometry())

        self.mainPage.setGeometry(
            QRect(0, 0, self.window.width(), self.window.height())
        )

        self.header.setGeometry(QRect(0, 70, self.window.width(), 50))

        self.awardsLayoutParent.setGeometry(
            QRect(0, 90, self.window.width(), self.window.height() - 90)
        )
        self.menuPushButton.setGeometry(
            int(0.02 * self.mainPage.width()), 50, int(0.1 * self.mainPage.width()), 70
        )

    def showData(self, data, pixmap):
        self.dialog = QDialog()

        self.dialog.setStyleSheet("background-color: #2E3440; margin: 50px")

        layout = QVBoxLayout()

        # Award Image
        label = QLabel()
        label.setFixedSize(200, 200)
        label.setScaledContents(True)
        label.setStyleSheet("background-color: transparent")
        label.setPixmap(pixmap)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Win Needed
        needed = QLabel()
        needed.setStyleSheet(
            "font-size: 20px; font-family: Comfortaa; color: #88C0D0;  margin: 10px"
        )
        needed.setText("Needed  :  " + str(data["needed"]))
        layout.addWidget(needed)

        # Info
        info = QLabel()
        info.setStyleSheet(
            "font-size: 20px; font-family: Comfortaa; color: #88C0D0;  margin: 10px"
        )
        info.setText("Info  :  " + str(data["info"]))
        layout.addWidget(info)

        # Has the challenger Won?
        won = QLabel()
        won.setStyleSheet(
            "font-size: 20px; font-family: Comfortaa; color: #88C0D0; margin: 10px"
        )
        won.setText("Has Won  :  " + str(data["won"]))
        layout.addWidget(won)

        # When the player has achieved?
        when = QLabel()
        when.setStyleSheet(
            "font-size: 20px; font-family: Comfortaa; color: #88C0D0; margin: 10px"
        )
        when.setText("Date  :  " + str(data["when"]))
        layout.addWidget(when)

        self.dialog.setLayout(layout)
        self.dialog.exec()
