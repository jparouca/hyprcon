from PySide6.QtWidgets import (QApplication, QDoubleSpinBox,  QGroupBox, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QWidget, QLabel, QSlider, QComboBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
import sys
from ..backend.hyprctl import HyprctlWrapper
from ..components.CToggleLabel import CToggleLabel


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
        pageTitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pageTitle.setStyleSheet("font-size: 20px; font-weight: semi-bold; margin-bottom: 20px;")
        

        self.mainLayout.addWidget(pageTitle)
        self.mainLayout.addWidget(self.mouseInteractionGroup())
        self.mainLayout.addWidget(self.layoutAndFocusGroup())

        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


    def mouseInteractionGroup(self):
        group = QGroupBox("Mouse Interaction and Sensitivity")
        layout = QVBoxLayout()
    
        
        # Sensitivity Option
        sensHLayout = QHBoxLayout()
        sensVLayout = QVBoxLayout()

        sensLabel = QLabel("Sensitivity (1.0 is recommended, legacy)")
        sensLabelFont = sensLabel.font()
        sensLabelFont.setPointSize(12)
        sensLabel.setFont(sensLabelFont)

        sensDescr = QLabel("mouse sensitivity (legacy, may cause bugs if not 1, prefer input:sensitivity)")
        sensDescrFont = sensDescr.font()
        sensLabelFont.setPointSize(9)
        sensDescr.setFont(sensDescrFont)
        sensVLayout.addWidget(sensLabel)
        sensVLayout.addWidget(sensDescr)
        
        sensSpinBox = QDoubleSpinBox()
        sensSpinBox.setRange(1.0, 0)
        sensSpinBox.setSingleStep(0.1)
        sensSpinBox.setValue(self.hyprctl.get_option(SECTION, "sensitivity", 'int'))
        sensSpinBox.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, "sensitivity", value))

        sensHLayout.addLayout(sensVLayout)
        sensHLayout.addStretch(1)
        sensHLayout.addWidget(sensSpinBox)

        layout.addLayout(sensHLayout)

        # Apply Sensitivity to Raw Mouse Output
        applySensToRawCheckbox = CToggleLabel("Apply sensitivity to raw mouse output (not recommended)",
                                              SECTION,
                                              'appy_sens_to_raw',
                                              'int',
                                              "if on, will also apply the sensitivity to raw mouse output (e.g. sensitivity in games)")

        layout.addWidget(applySensToRawCheckbox)

        # Resize on Border
        resizeOnBorderCheckbox = CToggleLabel("Resize on border",
                                              SECTION,
                                              'resize_on_border',
                                              'int',
                                              "enables resizing windows by clicking and dragging on borders and gaps")
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
        hoverIconOnBorderCheckbox = CToggleLabel("Hover icon on border",
                                                 SECTION,
                                                 'hover_icon_border',
                                                 'int',
                                                 "show a cursor icon when hovering over borders, only used when general:resize_on_border is on.")
        layout.addWidget(hoverIconOnBorderCheckbox)

        group.setLayout(layout)
        return group


    def layoutAndFocusGroup(self):
        group = QGroupBox("Layout and Focus")
        group.setStyleSheet("title {font-size: 15px; font-weight: semi-bold}")
        layout = QVBoxLayout()

        # Option: No Focus fallback
        focusFollowsMouseCheckbox = CToggleLabel("focus fallback", SECTION, 'no_focus_fallback', 'int')
        layout.addWidget(focusFollowsMouseCheckbox)

        # Option: no cursor warps
        autoTilingLayoutCheckbox = CToggleLabel("cursor warps", SECTION, 'no_cursor_warps', 'int')
        layout.addWidget(autoTilingLayoutCheckbox)

        # Option: Default Window Layout
        defaultLayoutLabel = QLabel("Default window layout:")
        defaultLayoutComboBox = QComboBox()
        defaultLayoutComboBox.addItems(["dwindle", "master"])
        defaultLayoutComboBox.setCurrentText(str(self.hyprctl.get_option(SECTION, "layout", 'str')))
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    hyprctl = HyprctlWrapper()
    window = GeneralPage()
    window.show()
    sys.exit(app.exec())
