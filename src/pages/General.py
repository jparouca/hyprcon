from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout, QGroupBox, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QWidget, QLabel, QSlider, QComboBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
import sys
from ..backend.hyprctl import HyprctlWrapper


SECTION = "general"

class GeneralPage(QMainWindow):
    def __init__(self):
        super(GeneralPage, self).__init__()
        self.hyprctl = HyprctlWrapper()

        mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(mainWidget)
        self.setCentralWidget(mainWidget)

        # Title
        pageTitle = QLabel("General")
        pageTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pageTitle.setStyleSheet("font-size: 20px; font-weight: semi-bold; margin-bottom: 20px;")
        

        self.mainLayout.addWidget(pageTitle)
        self.mainLayout.addWidget(self.mouseInteractionGroup())

        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def borderSizeComponent(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        container.setLayout(layout)

        title  = QLabel("Border size")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(self.hyprctl.get_option(SECTION, "border_size"))
        slider.setRange(0, 25)
        slider.setMaximumWidth(150)
        slider.setTickInterval(1)

        sliderValue = QLabel(str(slider.value()))
        slider.valueChanged.connect(lambda value: self.onSliderChange(sliderValue,"border_size", value))
        layout.addWidget(title)
        layout.addWidget(slider)
        layout.addWidget(sliderValue)

        return container


    def noBorderFloatingComponent(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        container.setLayout(layout)

        title = QLabel("No border on floating")

        combo = QComboBox()
        combo.addItem("true")
        combo.addItem("false")
        combo.setMaximumWidth(150)
        
        if self.hyprctl.get_option(SECTION, "no_border_floating") == 0:
            combo.setCurrentIndex(1) #false
        else:
            combo.setCurrentIndex(0)

        combo.currentTextChanged.connect(lambda: self.hyprctl.set_option(SECTION, "no_border_on_floating",  combo.currentText()))

        layout.addWidget(title)
        layout.addWidget(combo)

        return container

    def mouseInteractionGroup(self):
        group = QGroupBox("Mouse Interaction and Sensitivity")
        group.setStyleSheet("title {font-size: 15px; font-weight: semi-bold}")
        layout = QVBoxLayout()

        # Sensitivity Option
        sensLabel = QLabel("Sensitivity (1.0 is recommended, legacy)")
        sensSpinBox = QDoubleSpinBox()
        sensSpinBox.setRange(1.0, 0)
        sensSpinBox.setSingleStep(0.1)
        sensSpinBox.setValue(self.hyprctl.get_option(SECTION, "sensitivity"))
        sensSpinBox.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, "sensitivity", value))
        layout.addWidget(sensLabel)
        layout.addWidget(sensSpinBox)

        # Apply Sensitivity to Raw Mouse Output
        applySensToRawCheckbox = QCheckBox("Apply sensitivity to raw mouse output (not recommended)")
        applySensToRawCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "apply_sens_to_raw")))
        applySensToRawCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "apply_sens_to_raw", self.onCheckBoxChange(state)))

        layout.addWidget(applySensToRawCheckbox)

        # Resize on Border
        resizeOnBorderCheckbox = QCheckBox("Enable resizing windows by clicking and dragging on borders and gaps")
        resizeOnBorderCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "resize_on_border")))
        resizeOnBorderCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "resize_on_border", state == Qt.CheckState.Checked))

        layout.addWidget(resizeOnBorderCheckbox)

        # Extend Border Grab Area
        extendBorderGrabAreaLabel = QLabel("Extend border grab area (only when resizing on border is on)")
        extendBorderGrabAreaSlider = QSlider(Qt.Orientation.Horizontal)
        extendBorderGrabAreaSlider.setRange(0, 50)
        extendBorderGrabAreaSlider.setValue(bool(self.hyprctl.get_option(SECTION, "extend_border_grab_area")))
        extendBorderGrabAreaSlider.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, "extend_border_grab_area", value))

        layout.addWidget(extendBorderGrabAreaLabel)
        layout.addWidget(extendBorderGrabAreaSlider)

        # Hover Icon on Border
        hoverIconOnBorderCheckbox = QCheckBox("Show cursor icon when hovering over borders (only when resizing on border is on)")
        hoverIconOnBorderCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "hover_icon_on_border")))
        hoverIconOnBorderCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "hover_icon_on_border", state == Qt.CheckState.Checked))

        layout.addWidget(hoverIconOnBorderCheckbox)

        group.setLayout(layout)
        return group

    def onSliderChange(self, sliderValue, option, value):
        print(self.hyprctl.get_option(SECTION, option))
        sliderValue.setText(str(value))
        self.hyprctl.set_option(SECTION, option, value)


    def onCheckBoxChange(self, state):
        value = "true" if state == 2 else "false"
        self.hyprctl.set_option(SECTION, "apply_sens_to_raw", value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hyprctl = HyprctlWrapper()
    window = GeneralPage()
    window.show()
    sys.exit(app.exec())
