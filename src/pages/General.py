from PySide6.QtWidgets import  QVBoxLayout, QGroupBox, QLabel, QSpinBox, QWidget, QScrollArea, QDoubleSpinBox, QCheckBox, QLineEdit, QPushButton 
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from ..components.ColorPicker import ColorPicker
from ..backend.lib import QSpinBox, QDoubleSpinBox 


class MyLineEdit(QLineEdit):
    def wheelEvent(self, event):
        event.ignore()


class GeneralPage(QWidget):
    def __init__(self, IPCWrapper, parent=None):
        super(GeneralPage, self).__init__(parent)

        self.IPCWrapper = IPCWrapper
        self.CONF = self.IPCWrapper.getUserConf()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)

        # Create group boxes for different settings
        mouse_group = self.GroupContainer("Mouse", [("sensitivity", "Mouse Sens", QDoubleSpinBox, 1.0)])
        border_group = self.GroupContainer("Border", [("border_size", QSpinBox, 1), ("no_border_on_floating", QCheckBox, False)])
        gaps_group = self.GroupContainer("Gaps", [("gaps_in", QSpinBox, 5), ("gaps_out", QSpinBox, 20)])
        color_group = self.GroupContainer("Color", [("col.inactive_border", QPushButton, QColor("white")), ("col.active_border", QPushButton, QColor("black"))])
        cursor_group = self.GroupContainer("Cursor", [("cursor_inactive_timeout", QSpinBox, 0)])
        layout_group = self.GroupContainer("Layout", [("layout", QLineEdit, "dwindle")])

        # Add the group boxes to the main layout
        self.mainLayout.addWidget(mouse_group)
        self.mainLayout.addWidget(border_group)
        self.mainLayout.addWidget(gaps_group)
        self.mainLayout.addWidget(color_group)
        self.mainLayout.addWidget(cursor_group)
        self.mainLayout.addWidget(layout_group)

        self.scrollArea.setWidget(self.mainWidget)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scrollArea)

    def GroupContainer(self, title, section):
        group = QGroupBox(title)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 25, 0, 0)

        group.setLayout(layout)

        for setting, widgetClass, defaultValue in section:
            label = QLabel(setting['description'])
            layout.addWidget(label)

            if isinstance(defaultValue, bool):
                widget = QCheckBox()
            elif isinstance(defaultValue, int):
                widget = QSpinBox()
            elif isinstance(defaultValue, float):
                widget = QDoubleSpinBox()
            elif isinstance(defaultValue, str) and value.startswith('#'):
                widget = ColorPicker()
            else:
                continue

            widget.setValue(defaultValue)
            layout.addWidget(widget)


        return group

