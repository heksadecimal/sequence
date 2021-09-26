from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

class Animation:
    def fade(self , widget: QWidget):
        opacity = QGraphicsOpacityEffect()

        widget.setGraphicsEffect(opacity)

        animation = QPropertyAnimation(opacity , b"opacity")

        animation.setStartValue(1)

        animation.setEndValue(0)

        animation.setDuration(800)

        return animation
    
    def unfade(self , widget: QWidget):
        opacity = QGraphicsOpacityEffect()

        widget.setGraphicsEffect(opacity)

        animation = QPropertyAnimation(opacity , b"opacity")

        animation.setStartValue(0)

        animation.setEndValue(1)

        animation.setDuration(800)

        return animation

    