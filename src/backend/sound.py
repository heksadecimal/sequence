from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

bgSound = QSoundEffect()
igSound = QSoundEffect()

def playBG(sound="casino1", volume=1):
    bgSound.stop()

    file = f"../sounds/{sound}.wav"

    bgSound.setSource(QUrl.fromLocalFile(file))
    bgSound.setLoopCount(-2)
    bgSound.setVolume(volume)
    bgSound.play()

def changeVolBG(v):
    bgSound.setVolume(v)

#  ----------------------------------

def playIG(sound, volume=1):
    file = f"../sounds/{sound}.wav"
    igSound.stop()
    igSound.setSource(QUrl.fromLocalFile(file))
    igSound.setLoopCount(1)
    igSound.setVolume(volume)
    igSound.play()

def changeVolIG(v):
    igSound.setVolume(v)

