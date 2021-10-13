from typing import Any, Callable
from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    QVariantAnimation,
)
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget


class Animation:
    def fade(target: QWidget, duration: int) -> QPropertyAnimation:
        opacity = QGraphicsOpacityEffect()
        target.setGraphicsEffect(opacity)

        # QProperty Animation for the gradual decrease of the opacity
        opacityAnimation = QPropertyAnimation(opacity, b"opacity")
        opacityAnimation.setStartValue(1.0)
        opacityAnimation.setEndValue(0.0)
        opacityAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        opacityAnimation.setDuration(duration)

        return opacityAnimation

    def unfade(target: QWidget, duration: int) -> QPropertyAnimation:
        opacity = QGraphicsOpacityEffect()

        target.setGraphicsEffect(opacity)

        opacityAnimation = QPropertyAnimation(opacity, b"opacity")
        opacityAnimation.setStartValue(0.0)
        opacityAnimation.setEndValue(1.0)
        opacityAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        opacityAnimation.setDuration(duration)

        return opacityAnimation

    def variantAnimation(
        startValue: Any, endValue: Any, duration: int, callback: Callable
    ) -> QVariantAnimation:
        animation = QVariantAnimation()

        animation.setStartValue(startValue)
        animation.setEndValue(endValue)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.valueChanged.connect(callback)

        return animation

    def geometryAnimation(
        target: QWidget, endValue: QRect, duration: int
    ) -> QPropertyAnimation:
        geometryAnimation = QPropertyAnimation(target, b"geomtry")
        geometryAnimation.setStartValue(target.geometry())
        geometryAnimation.setEndValue(endValue)
        geometryAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        geometryAnimation.setDuration(duration)

        return geometryAnimation

    def moveAnimation(
        target: QWidget, endValue: QPoint, duration: int
    ) -> QPropertyAnimation:
        moveAnimation = QPropertyAnimation(target, b"pos")
        moveAnimation.setStartValue(target.pos())
        moveAnimation.setEndValue(endValue)
        moveAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        moveAnimation.setDuration(duration)

        return moveAnimation
