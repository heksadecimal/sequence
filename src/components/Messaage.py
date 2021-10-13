from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QRect, QTimer, Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget
from functools import partial


class Message:
    """

    # PyQtNotfy - A PyQt Ported Version For Notyf

    Notyf Source Code - https://github.com/caroso1222/notyf

    """

    def __init__(self, messageParent: QWidget) -> None:
        # Create an array for messages
        self.messages = []

        self.messageParent = messageParent

        self.types = {}

    def getALayout(self, msg: str) -> QHBoxLayout:
        layout = QHBoxLayout()

        layout.setContentsMargins(20, 0, 10, 0)

        icon = QLabel(text="")

        icon.setStyleSheet("font-size: 25px; color: #2E3440")

        icon.setFixedWidth(20)

        layout.addWidget(icon)

        content = QLabel()

        content.setText(msg)

        content.setStyleSheet("font-size: 15px; font-family: Comfortaa; font-weight: 1")

        content.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(content)

        return layout

    def success(self, renderWidget: QWidget = None) -> None:
        self.message = renderWidget

        self.message.setGeometry(
            QRect(10, self.messageParent.height() + 550, 320, 50)
        )  # 250 , 50

        self.message.setStyleSheet("background-color: #A3BE8C; border-radius: 5px")

        self.animation = QPropertyAnimation(self.message, b"pos")

        self.animation.setStartValue(self.message.pos())

        self.animation.setEndValue(QPoint(10, 930))

        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

        self.animation.setDuration(700)

        self.animation.start()

        self.message.show()

        QTimer.singleShot(2000, partial(self.hideMessage, self.message))

    def hideMessage(self, msg):
        self.animation = QPropertyAnimation(msg, b"pos")

        self.animation.setStartValue(msg.pos())

        self.animation.setEndValue(QPoint(10, self.messageParent.height() + 550))

        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

        self.animation.setDuration(700)

        self.animation.start()
