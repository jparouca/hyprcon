from PySide6.QtWidgets import QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget
from ..backend.hyprctl import HyprctlWrapper



class CSpinBoxLabel(QWidget):
    def __init__(self, text, SECTION, option, description=None):
        super().__init__()

        self.hyprctl = HyprctlWrapper()

        self.spin = CSpinBox()
        self.spin.setValue(int(self.hyprctl.get_option(SECTION, option, 'int')) * 100)
        self.spin.valueChanged.connect(lambda value, option: self.hyprctl.set_option(SECTION, option, value / 100.0))

        self.label = QLabel(text)
        self.labelFont = self.label.font()
        self.labelFont.setPointSize(12)
        self.label.setFont(self.labelFont)

        self.description = QLabel(description) if description else None

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.label)
        if self.description:
            descrFont = self.description.font()
            descrFont.setPointSize(9)
            descrFont.setItalic(True)
            self.description.setFont(descrFont)
            vLayout.addWidget(self.description)

        layout = QHBoxLayout()
        layout.addLayout(vLayout)
        layout.addStretch(1)
        layout.addWidget(self.spin)
        self.setLayout(layout)


class CSpinBox(QSpinBox):
    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()
