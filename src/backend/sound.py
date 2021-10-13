from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

bgSound = QSoundEffect()


def play(sound = "casino1", volume = 1):
    bgSound.stop()

    file = f"../sounds/{sound}.wav"

    bgSound.setSource(QUrl.fromLocalFile(file))
    bgSound.setLoopCount(-2)
    bgSound.setVolume(volume)
    bgSound.play()


def changeVol(v):
    bgSound.setVolume(v/100)
