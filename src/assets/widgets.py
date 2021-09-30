from PyQt6.QtGui import QColor, QEnterEvent, QMouseEvent
from PyQt6.QtWidgets import (
    QGraphicsColorizeEffect,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import (
    QParallelAnimationGroup,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
    pyqtSignal,
)


class QButton(QLabel):
    clicked = pyqtSignal()

    def __init__(self, window):
        super().__init__(window)

        self.currentColor = "#D8DEE9"

        self.setStyles()

        self.animation = QParallelAnimationGroup()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setStyles(self, f=True):
        self.setStyleSheet(
            """
            letter-spacing: 0.1em;
            font-size: 14px;
            font-weight: 400;
            line-height: 45px;
            text-decoration: none;
            text-transform: uppercase;
            width: 100%;
            color: {};
            border: 4px solid #2E3440;
            background-color: #2E3440;
        """.format(
                self.currentColor
            )
        )

        if f:
            opacity = QGraphicsOpacityEffect()

            opacity.setOpacity(0.9)

            self.setGraphicsEffect(opacity)

    def set_color(self, col):
        self.currentColor = col.name()

        print(self.currentColor)

        self.setStyles(False)

    color = pyqtProperty(QColor, fset=set_color)

    def enterEvent(self, event: QEnterEvent) -> None:

        # color = QGraphicsColorizeEffect()

        # self.setGraphicsEffect(color)

        # animation = QPropertyAnimation(color , b"color")

        # animation.setStartValue(QColor("#2E3440"));

        # animation.setEndValue(QColor("#D8DEE9"));

        # animation.setDuration(300);

        # self.animation.addAnimation(animation)

        # animation = QPropertyAnimation(self, b"color")

        # animation.setDuration(300)

        # animation.setStartValue(QColor("#D8DEE9"))

        # animation.setEndValue(QColor("#2E3440"))

        # self.animation.addAnimation(animation)

        # self.animation.start()
        pass

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        return super().mousePressEvent(ev)
