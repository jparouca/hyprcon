from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from .CToggle import CToggle
from ..backend.hyprctl import HyprctlWrapper



class CToggleLabel(QWidget):
    def __init__(self, text, SECTION, option, datatype, description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hyprctl = HyprctlWrapper()

        self.toggle = CToggle()

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
        layout.addWidget(self.toggle)
        self.setLayout(layout)

        self.toggle.setChecked(bool(self.hyprctl.get_option(SECTION, option, datatype)))
        self.toggle.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, option, 'true' if state == 2 else 'false'))


