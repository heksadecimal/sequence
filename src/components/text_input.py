from PyQt6.QtCore import QParallelAnimationGroup, QPointF, QRect, Qt , QEvent
from PyQt6.QtGui import QColor, QPaintEvent, QPainter, QPainterPath
from PyQt6.QtWidgets import QLabel, QLineEdit, QWidget
from assets.animations import Animation

class Triangle(QWidget):
    """Creates a triangular widget"""
    def __init__(self , parent: QWidget):
        # Initialize thre parent class
        super().__init__(parent)

        # Create an array of points 
        self.points = [QPointF(0 , 0) , QPointF(10 , 0) , QPointF(5 , 5)]

        # Color of the triangle
        self.color = "#4C566A"

    def getPath(self) -> QPainterPath:
        """Returns the path for making a triangle"""
        path = QPainterPath()

        path.moveTo(self.points[0])
        path.lineTo(self.points[1])
        path.lineTo(self.points[2])
        path.lineTo(self.points[0])

        return path

    def paintEvent(self, a0: QPaintEvent) -> None:
        # Get the path
        path = self.getPath()

        # Create a qpainter class
        painter = QPainter(self)

        # Fill the path
        painter.fillPath(path , QColor(self.color))

        return super().paintEvent(a0)

class Text_Input(QWidget):
    """A Modern PyQt6 Text Input"""
    def __init__(self , parent: QWidget , labelText: str , placeholder: str):
        # Initialize the super class
        super().__init__(parent)

        # Make args global
        self.labelText = labelText

        self.placeholder = placeholder

        self.activated = False

        # Run the render function
        self.drawInnerWidgets()

        # Set styles
        self.setStyles()

    def setStyles(self):
        # Set some stylings
        self.setStyleSheet("""
            background-color: #4C566A;
            color: #D8DEE9;
            border-radius: 5px
        """)

    def drawInnerWidgets(self):
        # A Left label which will display the text
        self.leftLabel = QLabel(self)

        # Set stylings
        self.leftLabel.setStyleSheet("background-color: #4C566A; border-radius: 0px; font-size: 12px; font-family: Comfortaa; font-weight: bold; border-top-left-radius: 10px; border-bottom-left-radius: 10px")

        # Set Geometry
        self.leftLabel.setGeometry(QRect(10 , 50 , 60 , 40))

        # Set the text
        self.leftLabel.setText(self.labelText)

        # Center Alignment (Vertically and Horizontally)
        self.leftLabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)

        # Create a tooltip triangle
        self.tooltipTriangle = Triangle(self)

        # Set geometry
        self.tooltipTriangle.setGeometry(QRect(33 , 80 , 70 , 70))

        # Show the tooltip
        self.tooltipTriangle.show()

        # Create an input box for taking input
        self.textEdit = QLineEdit(self)

        # Set geometry
        self.textEdit.setGeometry(QRect(10 , 50 , 520 , 40))

        # Set placeholder text
        self.textEdit.setText(self.placeholder)

        # Stack it under the span box (To prevent input hide the left label)
        self.textEdit.stackUnder(self.leftLabel)

        # Move tooltip up on mouse press 
        self.textEdit.mousePressEvent = self.moveLabelUp

        # Add some stylings
        self.textEdit.setStyleSheet("border-radius: 50px; padding-left: 60px")

        # Set height
        self.textEdit.setFixedHeight(40)

    def moveLabelUp(self , event):
        # Check if the tooltip is alread activated
        if(self.activated): return 

        # Set activated to true
        self.activated = True

        # Parallel Animation Group
        self.animation = QParallelAnimationGroup()

        # Set stylesheet
        self.leftLabel.setStyleSheet("border-radius: 8px")

        # Set stylesheet for the text input
        self.textEdit.setStyleSheet("border-radius: 4px; padding-left: 20px")

        # Move the left label above
        positionAnimation = Animation.geometryAnimation(self.leftLabel , QRect(self.leftLabel.x() , self.leftLabel.y() - 40 , self.leftLabel.width() , self.leftLabel.height() - 11) , 350)

        # Move the triangle along with the left label
        tooltipAnimation = Animation.geometryAnimation(self.tooltipTriangle , QRect(self.tooltipTriangle.x() , self.tooltipTriangle.y() - 42 , self.tooltipTriangle.width() , self.tooltipTriangle.height() - 11) , 350)

        # Add animation to parallel animation
        self.animation.addAnimation(tooltipAnimation)

        self.animation.addAnimation(positionAnimation)

        # Start the animation
        self.animation.start()
    
    def leaveEvent(self, a0: QEvent) -> None:
        # Check if the tooltip is activated
        if(not self.activated): return

        # Set activated to False
        self.activated = False

        # Parallel Animation Group
        self.animation = QParallelAnimationGroup()

        # Set the stylesheet of the left label
        self.leftLabel.setStyleSheet("border-radius: 8px")

        # Set text edit's stylesheet
        self.textEdit.setStyleSheet("border-radius: 4px; padding-left: 60px")

        # Animation for reseting the position of both the elements
        positionAnimation = Animation.geometryAnimation(self.leftLabel , QRect(10 , 50 , 60 , 40) , 350)

        tooltipAnimation = Animation.geometryAnimation(self.tooltipTriangle , QRect(33 , 80 , 70 , 70) , 350)

        # Add animations to the parallel animation grouo
        self.animation.addAnimation(tooltipAnimation)

        self.animation.addAnimation(positionAnimation)

        # Start the animation
        self.animation.start()

        return super().leaveEvent(a0)