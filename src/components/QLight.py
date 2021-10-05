from PyQt6.QtCore import QEvent
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent 
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget
from components.AngledLabel import AngledLabel

class QLightReflectionButton(QLabel):
    """A Light Reflection """
    # Signal for user click
    clicked = pyqtSignal()

    def __init__(self , parent: QWidget) -> None:
        super().__init__(parent)

        # Set default styles to the button
        self.setStyles()

        # Center Align The Text (both vertically and horizontally)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)

        # Pointing Hand Cursor
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Show the button
        self.show()

    def setStyles(self):
        # Stylings
        self.setStyleSheet("""
            QLabel{
                letter-spacing: 0.1em;
                font-size: 14px;
                font-weight: 400;
                line-height: 45px;
                text-decoration: none;
                text-transform: uppercase;
                width: 100%;
                color: #FFF;
                border-radius: 10px;
                border: 4px solid #4C566A;
                background-color: #4C566A;
            }

            QLabel:hover{
                border: 4px solid #2E3440;
                background-color: #4C566A;
            }
        """)

        # Create an instance of Angled Label
        self.lightReflection = AngledLabel(self)

        # Remove the border radius (It is applied because of its parent's stylings)
        self.lightReflection.setStyleSheet("border-radius: 0px")

        # Move the light reflection on top of the parent
        self.lightReflection.stackUnder(self)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # Check if the press event was with the left mouse button
        if(ev.button() == Qt.MouseButton.LeftButton):

            # Send the signal
            self.clicked.emit()

        return super().mousePressEvent(ev)

    def leaveEvent(self, a0: QEvent) -> None:
        # Reset animation when the user leaves the button
        self.lightReflection.reset()

        return super().leaveEvent(a0)