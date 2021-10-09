# Import all the required modules
from typing import Any
from PyQt6.QtCore import QPointF, QSequentialAnimationGroup, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QEnterEvent, QMouseEvent , QTransform
from PyQt6.QtWidgets import QGraphicsColorizeEffect, QGraphicsScene, QGraphicsView, QWidget
from functools import partial
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from assets.animations import Animation

class Rounded_Jolly_Button(QGraphicsView):
    # Signal for listening for user clicks
    clicked = pyqtSignal()
    
    def __init__(self , parent: QWidget , location: str , size: QSize = QSize(45 , 45) , padding: QPointF = QPointF(10 , 10)):
        # Initialize the parent class
        super().__init__(parent)

        # Make icon location global
        self.location = location

        self.padding = padding

        # Add in some stylings
        self.setStyleSheet("background-color: #2E3440; border-radius: {}px".format(size.width() // 2))

        # Set the position
        self.setFixedSize(size)

        # Pointing Hand cursor
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create a scene
        self._scene = QGraphicsScene()

        # Set the scene
        self.setScene(self._scene)

        # Set scene rect
        self._scene.setSceneRect(0 , 0 , 40 , 40)

        # Remove scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Set stylings
        self.setStyles()

    def setStyles(self):
        # Color for the svg
        color = QGraphicsColorizeEffect()

        # Set the color
        color.setColor(QColor("#D8DEE9"))

        # Create an svg graphics item class
        svg = QGraphicsSvgItem(self.location)

        # Accept hover events
        svg.setAcceptHoverEvents(True)

        # Move to the center
        svg.setPos(self.padding)

        # Set the color of the svg
        svg.setGraphicsEffect(color)

        # Add svg to the scene
        self._scene.addItem(svg)

        # Set the transformation point to center
        svg.setTransformOriginPoint(svg.boundingRect().center())

        # Sequential Animation group
        self.animations = QSequentialAnimationGroup()

        # Animations required for the effect
        self.animations.addAnimation(Animation.variantAnimation(QPointF(1.0 , 1.0) , QPointF(1.25 , 0.75) , 270 , partial(self.updateTransform , svg)))

        self.animations.addAnimation(Animation.variantAnimation(QPointF(1.25 , 0.75) , QPointF(.75 , 1.25) , 90 , partial(self.updateTransform , svg)))

        self.animations.addAnimation(Animation.variantAnimation(QPointF(.75 , 1.25) , QPointF(1.15 , .85) , 90 , partial(self.updateTransform , svg)))

        self.animations.addAnimation(Animation.variantAnimation(QPointF(1.15 , 0.85) , QPointF(.95 , 1.05) , 135 , partial(self.updateTransform , svg)))

        self.animations.addAnimation(Animation.variantAnimation(QPointF(.95 , 1.05) , QPointF(1.05 , 0.95) , 90 , partial(self.updateTransform , svg)))

        self.animations.addAnimation(Animation.variantAnimation(QPointF(1.05 , 0.95) , QPointF(1 , 1) , 225 , partial(self.updateTransform , svg)))

    def enterEvent(self, event: QEnterEvent) -> None:
        # Run the animation on hover
        self.animations.start()

        return super().enterEvent(event)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # Check for mouse clicks
        if(ev.button() == Qt.MouseButton.LeftButton):
            # Emit the clicked event
            self.clicked.emit()

        return super().mousePressEvent(ev)

    def updateTransform(self , target: QGraphicsSvgItem , newValue: Any):
        origin = target.transformOriginPoint()

        transform = QTransform().translate(origin.x(), origin.y())

        transform.scale(newValue.x(), newValue.y())

        transform.translate(-origin.x(), -origin.y())

        target.setTransform(transform)
