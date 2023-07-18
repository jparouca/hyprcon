from PySide6.QtWidgets import QColorDialog, QPushButton
from PySide6.QtGui import QColor

class ColorPicker(QPushButton):
    def __init__(self, parent=None):
        super(ColorPicker, self).__init__(parent)
        self.clicked.connect(self.pick_color)
        self.color = QColor()

    def pick_color(self):
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.setStyleSheet(f"background-color: {color.name()}")

    def setValue(self, color):
        self.color = QColor(color)
        self.setStyleSheet(f"background-color: {color}")

