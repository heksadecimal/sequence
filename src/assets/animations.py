from typing import Any, Callable
from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QRect, QVariantAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

class Animation:
    def fade(target: QWidget, duration: int) -> QPropertyAnimation:
        # Opacity
        opacity = QGraphicsOpacityEffect()

        # Set the graphics effect to the target
        target.setGraphicsEffect(opacity)

        # QProperty Animation for the gradual decrease of the opacity
        opacityAnimation = QPropertyAnimation(opacity , b"opacity")

        # Start with the widget with a opacity of 1
        opacityAnimation.setStartValue(1.0)

        # End with the widget having an opacity of 0 (hidden)
        opacityAnimation.setEndValue(0.0)

        # Smooth, easing curves
        opacityAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Set duration
        opacityAnimation.setDuration(duration)

        return opacityAnimation

    def unfade(target: QWidget , duration: int) -> QPropertyAnimation:
        # Initiate the opacity class
        opacity = QGraphicsOpacityEffect()

        # Set the graphics effect to the target
        target.setGraphicsEffect(opacity)

        # QProperty Animation for the gradual decrease of the opacity
        opacityAnimation = QPropertyAnimation(opacity , b"opacity")

        # Start with the widget with a opacity of 1
        opacityAnimation.setStartValue(0.0)

        # End with the widget having an opacity of 0 (hidden)
        opacityAnimation.setEndValue(1.0)

        # Smooth, easing curves
        opacityAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Set duration
        opacityAnimation.setDuration(duration)

        return opacityAnimation

    def variantAnimation(startValue: Any , endValue: Any , duration: int , callback: Callable) -> QVariantAnimation:
        # Create a varint animation instance
        animation = QVariantAnimation()

        # Set the startb value
        animation.setStartValue(startValue)

        # Set the end value
        animation.setEndValue(endValue)

        # Set the duration
        animation.setDuration(duration)

        # Set Easing curve
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Call the callback on update function
        animation.valueChanged.connect(callback)

        # Return the animation
        return animation

    def geometryAnimation(target: QWidget , endValue: QRect , duration: int) -> QPropertyAnimation:
        # QProperty Animation for a smooth animation
        geometryAnimation = QPropertyAnimation(target , b"geomtry")

        # Set the original value as the current geometry of the target
        geometryAnimation.setStartValue(target.geometry())

        # Set the end value as provided
        geometryAnimation.setEndValue(endValue)

        # Smooth, easing curves
        geometryAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Set duration
        geometryAnimation.setDuration(duration)

        return geometryAnimation

    def moveAnimation(target: QWidget , endValue: QPoint , duration: int) -> QPropertyAnimation:
        # QProperty Animation for a smooth animation
        moveAnimation = QPropertyAnimation(target , b"pos")

        # Set the original value as the current geometry of the target
        moveAnimation.setStartValue(target.pos())

        # Set the end value as provided
        moveAnimation.setEndValue(endValue)

        # Smooth, easing curves
        moveAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Set duration
        moveAnimation.setDuration(duration)

        return moveAnimation
