from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox

class QSpinBox(QSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class QDoubleSpinBox(QDoubleSpinBox):
    def wheelEvent(self, event):
        event.ignore()

