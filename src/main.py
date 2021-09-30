from views.game import Game_Renderer
from views.settings import Settings_Renderer
from views.statistics import Statistics_Renderer
from views.awards import Award_Renderer
from views.profile import Profile_Renderer
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow


class Main:
    def __init__(self, window: QMainWindow) -> None:
        self.window = window

    def create(self):
        # Profile Render
        self.window.setCentralWidget(Profile_Renderer(self.window).render())

        # Awards Render
        # self.window.setCentralWidget(Award_Renderer(self.window).render())

        # Statistics Render
        # self.window.setCentralWidget(Statistics_Renderer(self.window).render())

        # Settings Renderer
        # self.window.setCentralWidget(Settings_Renderer(self.window).render())

        # Game Render
        # self.window.setCentralWidget(Game_Renderer(self.window).render())


if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    window.setStyleSheet("background-color: #2E3440")
    renderer = Main(window)
    renderer.create()
    window.show()
    exit(app.exec())
