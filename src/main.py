from functools import partial

from PyQt6.QtGui import QCloseEvent
from views.game import Game_Renderer
from views.settings import Settings_Renderer
from views.statistics import Statistics_Renderer
from views.awards import Award_Renderer
from views.profile import Profile_Renderer
from PyQt6.QtCore import QPoint, QRect, QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QMainWindow,
    QPushButton,
)

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect


class Main:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.quit = 0
        
    def create(self):
        self.window.setCentralWidget(Profile_Renderer(self.window).render())

    def cleanClose(self, event: QCloseEvent):
        self.ok = QDialog(self.window)
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
        self.quitLabel.setText("Do you wish to quit the game ?")
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
        self.yes.clicked.connect(exit)
        self.no.clicked.connect(self.ok.hide)
        self.quitLabel.show()
        self.ok.exec()
        event.ignore()


if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    window.setStyleSheet("background-color: #2E3440")
    renderer = Main(window)
    window.closeEvent = renderer.cleanClose
    renderer.create()
    window.show()
    exit(app.exec())
