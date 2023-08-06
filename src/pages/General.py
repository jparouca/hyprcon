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
        self.mainLayout.addWidget(self.layoutAndFocusGroup())

        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


    def mouseInteractionGroup(self):
        group = QGroupBox("Mouse Interaction and Sensitivity")
        group.setStyleSheet("title {font-size: 15px; font-weight: semi-bold}")
        layout = QVBoxLayout()

        # Sensitivity Option
        sensLabel = QLabel("Sensitivity (1.0 is recommended, legacy)")
        sensSpinBox = QDoubleSpinBox()
        sensSpinBox.setRange(1.0, 0)
        sensSpinBox.setSingleStep(0.1)
        sensSpinBox.setValue(self.hyprctl.get_option(SECTION, "sensitivity", 'int'))
        sensSpinBox.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, "sensitivity", value))
        layout.addWidget(sensLabel)
        layout.addWidget(sensSpinBox)

        # Apply Sensitivity to Raw Mouse Output
        applySensToRawCheckbox = QCheckBox("Apply sensitivity to raw mouse output (not recommended)")
        applySensToRawCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "apply_sens_to_raw", 'int')))
        applySensToRawCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "apply_sens_to_raw", self.onCheckBoxChange(state)))

        layout.addWidget(applySensToRawCheckbox)

        # Resize on Border
        resizeOnBorderCheckbox = QCheckBox("Enable resizing windows by clicking and dragging on borders and gaps")
        resizeOnBorderCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "resize_on_border", 'int')))
        resizeOnBorderCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "resize_on_border", "true" if state == 2 else "false"))

        layout.addWidget(resizeOnBorderCheckbox)

        # Extend Border Grab Area
        extendBorderGrabAreaLabel = QLabel("Extend border grab area (only when resizing on border is on)")
        extendBorderGrabAreaSlider = QSlider(Qt.Orientation.Horizontal)
        extendBorderGrabAreaSlider.setRange(0, 50)
        extendBorderGrabAreaSlider.setValue(bool(self.hyprctl.get_option(SECTION, "extend_border_grab_area", 'int')))
        extendBorderGrabAreaSlider.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, "extend_border_grab_area", value))

        layout.addWidget(extendBorderGrabAreaLabel)
        layout.addWidget(extendBorderGrabAreaSlider)

        # Hover Icon on Border
        hoverIconOnBorderCheckbox = QCheckBox("Show cursor icon when hovering over borders (only when resizing on border is on)")
        hoverIconOnBorderCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "hover_icon_on_border", 'int')))
        hoverIconOnBorderCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "hover_icon_on_border", "true" if state == 2 else "false"))

        layout.addWidget(hoverIconOnBorderCheckbox)

        group.setLayout(layout)
        return group


    def layoutAndFocusGroup(self):
        group = QGroupBox("Layout and Focus")
        group.setStyleSheet("title {font-size: 15px; font-weight: semi-bold}")
        layout = QVBoxLayout()

        # Option: No Focus fallback
        focusFollowsMouseCheckbox = QCheckBox("focus fallback")
        focusFollowsMouseCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "no_focus_fallback", 'int')))
        focusFollowsMouseCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "no_focus_fallback", "true" if state == 2 else "false"))
        layout.addWidget(focusFollowsMouseCheckbox)

        # Option: no cursor warps
        autoTilingLayoutCheckbox = QCheckBox("cursor warps")
        autoTilingLayoutCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "no_cursor_warps", 'int')))
        autoTilingLayoutCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "no_cursor_warps", "true" if state == 2 else "false"))
        layout.addWidget(autoTilingLayoutCheckbox)

        # Option: Default Window Layout
        defaultLayoutLabel = QLabel("Default window layout:")
        defaultLayoutComboBox = QComboBox()
        defaultLayoutComboBox.addItems(["dwindle", "master"])
        defaultLayoutComboBox.setCurrentText(self.hyprctl.get_option(SECTION, "layout", 'str'))
        defaultLayoutComboBox.currentTextChanged.connect(lambda text: self.hyprctl.set_option(SECTION, "layout", text))
        defaultLayoutHBox = QHBoxLayout()
        defaultLayoutHBox.addWidget(defaultLayoutLabel)
        defaultLayoutHBox.addWidget(defaultLayoutComboBox)
        layout.addLayout(defaultLayoutHBox)

        group.setLayout(layout)
        return group



    def onSliderChange(self, sliderValue, option, value):
        print(self.hyprctl.get_option(SECTION, option, 'int'))
        sliderValue.setText(str(value))
        self.hyprctl.set_option(SECTION, option, value)


    def onCheckBoxChange(self, state):
        if state is not None:
            self.hyprctl.set_option(SECTION, "apply_sens_to_raw", "true" if state == 2 else "false")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    hyprctl = HyprctlWrapper()
    window = GeneralPage()
    window.show()
    sys.exit(app.exec())
