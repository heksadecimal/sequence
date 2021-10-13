from backend.sound import play
from views.menu import MenuRenderer

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QMainWindow,
    QPushButton,
)


class Main:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        play()
        self.quit = 0

    def create(self):
        self.window.setCentralWidget(MenuRenderer(self.window).render())

    def cleanClose(self, event: QCloseEvent):
        self.closeDialog = QDialog(self.window)
        self.closeDialog.setWindowTitle("Quit Sequece")
        self.closeDialog.setGeometry(
            0.4 * self.window.geometry().width(),
            0.4 * self.window.geometry().height(),
            500,
            200,
        )
        self.closeDialog.setStyleSheet("background-color: #3b4252")

        self.quitLabel = QLabel(self.closeDialog)
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

        self.yes = QPushButton(self.closeDialog)
        self.yes.setText("YES")
        self.yes.setGeometry(
            self.yes.geometry().x() + 100,
            self.yes.geometry().y() + 120,
            self.yes.geometry().width(),
            self.yes.geometry().height(),
        )
        self.yes.show()

        self.no = QPushButton(self.closeDialog)
        self.no.setText("NO")
        self.no.setGeometry(
            self.no.geometry().x() + 250,
            self.no.geometry().y() + 120,
            self.no.geometry().width(),
            self.no.geometry().height(),
        )
        self.no.show()
        self.yes.clicked.connect(exit)
        self.no.clicked.connect(self.closeDialog.hide)
        self.quitLabel.show()
        self.closeDialog.exec()
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
