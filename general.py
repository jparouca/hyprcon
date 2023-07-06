from ctypes import alignment
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QHBoxLayout, QSlider, QSpinBox, QVBoxLayout, QWidget, QLabel,  QCheckBox


class GeneralPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(ToggleContainer('Border on Floating',
                                         'disable borders for floating windows'))
        layout.addWidget(ToggleContainer("Cursor Warp",
                                         "if on, will warp the cursor to the center of the window when switching to a new window"))
        layout.addWidget(ToggleContainer("Focus Fallback",
                                         'if true will not fall back to the next available window when moving focus in a direction where no window was found'))
        layout.addWidget(ToggleContainer('Apply Sens to Raw',
                                         'if on, will also apply the sensitivity to raw mouse output (e.g. sensitivity in games) NOTICE: really not recommended.'))
        layout.addWidget(ToggleContainer('Resize on Border',
                                         'enables resizing windows by clicking and dragging on borders and gaps'))
        layout.addWidget(ToggleContainer('Hover icon on Border',
                                         'show a cursor icon when hovering over borders, only used when general:resize_on_border is on.'))
        layout.addWidget(SpinBoxContainer('Rounded Corners Radius',
                                          'rounded corners’ radius (in layout px)',
                                          0, 50, 0))
        layout.addWidget(SpinBoxContainer('Blur Size',
                                          'blur size (distance)',
                                          0, 50, 8))
        layout.addWidget(SpinBoxContainer('Blur Passes',
                                          'the amount of passes to perform',
                                          0, 5, 1))
        layout.addWidget(SpinBoxContainer('Shadow Range',
                                          'Shadow range (“size”) in layout px',
                                          0, 20, 4))
        layout.addWidget(SpinBoxContainer('Shadow Range',
                                          '(1 - 4), in what power to render the falloff (more power, the faster the falloff)',
                                          1, 4, 3))
        layout.addWidget(SliderContainer('Active Opacity',
                         'opacity of active windows. (0.0 - 1.0)',
                         0.0, 1.0, 1.0))

        layout.addStretch(1)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)



class Toggle(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setFixedSize(60, 30)
        self.stateChanged.connect(print("state change"))
        self.setStyleSheet("""
                           QCheckBox {
                               background: #bfbfbf;
                               border-radius: 10px;
                               padding: 3px;
                               }
                           QCheckBox::indicator {
                               background: white;
                               border-radius: 10px;
                               width: 20px;
                               height: 20px;
                               }
                           QCheckBox:checked {
                               background: #4CAF50;
                               }
                           QCheckBox:checked::indicator {
                               margin-left: 30px;
                               }
                           """)

@Slot(int)
def handle_state_change(self, state):
    self.valueChanged.emit(state ==2)


class ToggleContainer(QWidget):
    def __init__(self, name, description):
        super().__init__()
        
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel(name))
        v_layout.addWidget(QLabel(description))

        layout = QHBoxLayout()
        layout.addLayout(v_layout)
        layout.addStretch(1)
        layout.addWidget(Toggle())

        self.setLayout(layout)


class SpinBoxContainer(QWidget):
    def __init__(self, name, description, min_value, max_value, default_value):
        super().__init__()

        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel(name))
        v_layout.addWidget(QLabel(description))

        self.spinBox = QSpinBox()
        self.spinBox.setRange(min_value, max_value)
        self.spinBox.setValue(default_value)

        layout = QHBoxLayout()
        layout.addLayout(v_layout)
        layout.addStretch(1)
        layout.addWidget(self.spinBox)

        self.setLayout(layout)



class SliderContainer(QWidget):
    def __init__(self, name, description, min_value, max_value, default_value):
        super().__init__()

        self.scale = 100.0  # Scale factor

        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel(name))
        v_layout.addWidget(QLabel(description))


        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(min_value * self.scale)
        self.slider.setMaximum(max_value * self.scale)
        self.slider.setValue(default_value * self.scale)
        self.slider.valueChanged.connect(self.handleSliderChange)

        layout = QHBoxLayout()
        layout.addLayout(v_layout)
        layout.addStretch(1)
        self.value_label = QLabel('1.0')
        layout.addWidget(self.value_label)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    @Slot()
    def handleSliderChange(self):
        value = self.slider.value() / self.scale
        self.value_label.setText(str(value))

