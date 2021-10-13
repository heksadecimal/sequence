from PyQt6.QtCore import QParallelAnimationGroup
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QTimer
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QGraphicsView, QLabel, QGraphicsScene, QGraphicsProxyWidget
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtWidgets import QWidget
from assets.animations import Animation

# Class AngledLabel
class AngledLabel(QWidget):
    """A tilted / angled label"""

    def __init__(self, parent: QWidget) -> None:
        # Initiate super class
        super(AngledLabel, self).__init__(parent)

        # Render the angled label
        self.render()

    def render(self) -> None:
        """Renders the label to the parent"""
        # Create a label
        label = QLabel()

        # Give it a size of 1000x100
        label.setFixedSize(1000, 100)

        # Move to top left (x: 0 , y: 0)
        label.move(0, 0)

        # Stylings
        label.setStyleSheet(
            "padding: 40px; background-color: #D8DEE9; border-radius: 10px"
        )

        # Creating a graphics view
        self.graphicsview = QGraphicsView(self)

        # A Scene where the widgets will be added
        scene = QGraphicsScene()

        # Set the scene
        self.graphicsview.setScene(scene)

        # MOve the scrolls on enter event (Moving scrolls gives the light reflection effect, because of the height and angle of the widget)
        self.graphicsview.enterEvent = self.moveScrolls

        # Remove / Hide scrollbars
        self.graphicsview.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.graphicsview.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # A Proxy Widget
        proxy = QGraphicsProxyWidget()

        # Set the widget to the label
        proxy.setWidget(label)

        # Set the transformation point to center (both vertically and horizontally)
        proxy.setTransformOriginPoint(proxy.boundingRect().center())

        # Add item to the scene
        scene.addItem(proxy)

        # Move the widget
        proxy.setPos(10, 10)

        # Rotate the widget (45deg anticlockwise)
        proxy.setRotation(-45)

        # Set the geometry of the graphics
        self.graphicsview.setGeometry(QRect(0, 0, 610, 70))

        # Stylings
        self.graphicsview.setStyleSheet(
            "background-color: transparent; border-radius: 10px"
        )

        # Set the values of the scollbar at a certain position, so that the widget is kept hidden unless the user hovers it
        QTimer.singleShot(
            0,
            lambda: self.graphicsview.verticalScrollBar().setValue(
                self.graphicsview.verticalScrollBar().maximum()
            ),
        )

        QTimer.singleShot(
            0,
            lambda: self.graphicsview.horizontalScrollBar().setValue(
                self.graphicsview.horizontalScrollBar().maximum()
            ),
        )

    def moveScrolls(self, event: QEnterEvent) -> None:
        "Move scrolls to bottom right so as to create an animation (light reflection)"
        # A Parallel Animation class instance
        self.animations = QParallelAnimationGroup()

        # Create an animation for the smooth movement of the scrollbar
        animationMoving = QPropertyAnimation(
            self.graphicsview.verticalScrollBar(), b"value"
        )

        # Set the start value of the animation as the current value of the property of the target
        animationMoving.setStartValue(self.graphicsview.verticalScrollBar().value())

        # Set end value
        animationMoving.setEndValue(-270)

        # Easing Curve, Start and Ending slow and rest fast
        animationMoving.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Duration
        animationMoving.setDuration(600)

        # Add animation to the parallel animation instance
        self.animations.addAnimation(animationMoving)

        # Opacity animation
        opacityAnimation = Animation.fade(self.graphicsview, 600)

        # Add animation to the parallel animation class
        self.animations.addAnimation(opacityAnimation)

        # Start the animation
        self.animations.start()

    def reset(self) -> None:
        self.animations = QParallelAnimationGroup()

        # Animation for moving the scrollbars
        animationMoving = QPropertyAnimation(
            self.graphicsview.verticalScrollBar(), b"value"
        )

        # Set start value
        animationMoving.setStartValue(-290)

        # Set end value
        animationMoving.setEndValue(self.graphicsview.verticalScrollBar().maximum())

        # Set easing curve
        animationMoving.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Set duration
        animationMoving.setDuration(600)

        # Add the animation to the parallel animation group
        self.animations.addAnimation(animationMoving)

        # Hide the light reflection parallely
        self.animations.addAnimation(Animation.unfade(self.graphicsview, 600))

        # Start the animation
        self.animations.start()
