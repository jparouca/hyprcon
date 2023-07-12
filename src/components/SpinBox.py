from PySide6.QtWidgets import QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget


class SpinBoxContainer(QWidget):
    def __init__(self, name, description, min_value, max_value, default_value):
        super().__init__()

        name = QLabel(name)
        name.setObjectName('name')
        description = QLabel(description)
        description.setObjectName('description')

        v_layout = QVBoxLayout()
        v_layout.addWidget(name)
        v_layout.addWidget(description)

        self.spinBox = QSpinBox()
        self.spinBox.setRange(min_value, max_value)
        self.spinBox.setValue(default_value)

        layout = QHBoxLayout()
        layout.addLayout(v_layout)
        layout.addStretch(1)
        layout.addWidget(self.spinBox)


        # Style
        self.spinBox.setObjectName('spinbox)')
        self.spinBox.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)


        self.setLayout(layout)

        # style
        self.setObjectName('spinbox-container')
        



