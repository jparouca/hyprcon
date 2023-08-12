from PySide6.QtCore import Qt

from PySide6.QtWidgets import QSlider


class CSlider(QSlider):
    def __init__(self):
        super(CSlider, self).__init__() 
        
        #set orientattion
        self.setOrientation(Qt.Orientation.Horizontal)

    def wheelEvent(self, event):
        if self.hasFocus():
            super(CSlider, self).wheelEvent(event)
        else:
            event.ignore()
