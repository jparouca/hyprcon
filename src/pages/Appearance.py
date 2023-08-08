from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QCheckBox, QColorDialog, QDoubleSpinBox, QHBoxLayout,  QLineEdit, QMainWindow, QSizePolicy, QSlider, QSpacerItem, QSpinBox, QVBoxLayout, QGroupBox, QLabel,  QWidget
from ..backend.hyprctl import HyprctlWrapper


SECTION = "decoration"

class AppearancePage(QMainWindow):
    def __init__(self, parent=None):
        super(AppearancePage, self).__init__(parent)
        self.hyprctl = HyprctlWrapper()

        mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(mainWidget)
        self.setCentralWidget(mainWidget)

        pageTitle = QLabel("Appearance")
        pageTitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pageTitle.setStyleSheet("font-size: 20px; color: #344054; font-weight: semi-bold; margin-bottom: 20px;")

        self.mainLayout.addWidget(pageTitle)
        self.mainLayout.addWidget(self.antialiasingAndOpacityGroup())
        self.mainLayout.addWidget(self.shadowGroup())
        self.mainLayout.addWidget(self.dimGroup())

        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def antialiasingAndOpacityGroup(self):
        group = QGroupBox("Antialiasing and Opacity")
        layout = QVBoxLayout()

        # multisample_edges
        multisampleEdgesCheckbox = QCheckBox("Enable antialiasing (no-jaggies) for rounded corners")
        multisampleEdgesCheckbox.setChecked(bool(self.hyprctl.get_option(SECTION, "multisample_edges", 'int')))
        multisampleEdgesCheckbox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, "multisample_edges", state == Qt.CheckState.Checked))
        layout.addWidget(multisampleEdgesCheckbox)

        # active_opacity, inactive_opacity, fullscreen_opacity
        for opacity_option, description in zip(['active_opacity', 'inactive_opacity', 'fullscreen_opacity'],
                                               ['Opacity of active windows', 'Opacity of inactive windows', 'Opacity of fullscreen windows']):
            opacitySlider = QSlider(Qt.Orientation.Horizontal)
            opacitySlider.setRange(0, 100)
            opacitySlider.setValue(int(float(self.hyprctl.get_option(SECTION, opacity_option, 'float')) * 100))
            opacitySlider.valueChanged.connect(lambda value, option=opacity_option: self.hyprctl.set_option(SECTION, option, value / 100.0))
            layout.addWidget(QLabel(description))
            layout.addWidget(opacitySlider)

        group.setLayout(layout)
        return group


    def shadowGroup(self):
        group = QGroupBox("Shadows")
        layout = QVBoxLayout()

        # drop shadow and shadow ignore window
        hLayout = QHBoxLayout()
        dropShadowCheckBox = QCheckBox("Enable drop shadow")
        dropShadowCheckBox.setChecked(bool(self.hyprctl.get_option(SECTION, "drop_shadow", 'int')))
        dropShadowCheckBox.stateChanged.connect((lambda state: self.hyprctl.set_option(SECTION, 'drop_shadow', 'true' if state == 2 else 'false')))
        hLayout.addWidget(dropShadowCheckBox)

        shadowIgnoreCheckBox = QCheckBox("window ignore (if true the shadow will not be rendered behind the window, only around it)")
        shadowIgnoreCheckBox.setChecked(bool(self.hyprctl.get_option(SECTION, 'shadow_ignore_window', 'int')))
        shadowIgnoreCheckBox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, 'shadow_ignore_window', 'true' if state == 2 else 'false'))
        hLayout.addWidget(shadowIgnoreCheckBox)
        layout.addLayout(hLayout)

        # shadow range in pixels (add a interval for ticket)
        shadowRangeLabel = QLabel("Shadow range (in px)")
        shadowRangeSpinBox = QSpinBox()
        shadowRangeSpinBox.setRange(0, 100)
        shadowRangeSpinBox.setValue(int(self.hyprctl.get_option(SECTION, "shadow_range", 'int')))
        shadowRangeSpinBox.valueChanged.connect((lambda value: self.hyprctl.set_option(SECTION, 'shadow_range', value)))
        layout.addWidget(shadowRangeLabel)
        layout.addWidget(shadowRangeSpinBox)

        # shadow render power (1 - 4)
        shadowRenderLabel = QLabel("Shadow render power (more power = faster fallout)")
        shadowRenderPowerSpinBox = QSpinBox()
        shadowRangeSpinBox.setRange(1, 4)
        shadowRenderPowerSpinBox.setValue(int(self.hyprctl.get_option(SECTION, 'shadow_render_power', 'int')))
        shadowRenderPowerSpinBox.valueChanged.connect(lambda state: self.hyprctl.set_option(SECTION, 'shadow_render_power', state))
        layout.addWidget(shadowRenderLabel)
        layout.addWidget(shadowRenderPowerSpinBox)

        # shadow ignore window

        # shadow scale
        shadowScaleLabel = QLabel("Shadow scale (1.0 = 100%)")
        shadowScaleSpin = QDoubleSpinBox()
        shadowScaleSpin.setRange(0.0, 1.0)
        shadowScaleSpin.setSingleStep(0.1)
        shadowScaleSpin.setValue(float(self.hyprctl.get_option(SECTION, 'shadow_scale', 'float')))
        shadowScaleSpin.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, 'shadow_scale', value))
        layout.addWidget(shadowScaleLabel)
        layout.addWidget(shadowScaleSpin)

        group.setLayout(layout)

        return group


    def dimGroup(self):
        group = QGroupBox("Dim")
        layout = QVBoxLayout()
        group.setLayout(layout)


        hLayout = QHBoxLayout()
        # Dim Inactive
        dimInactiveCheckBox = QCheckBox("Dim inactive windows")
        dimInactiveCheckBox.setChecked(bool(self.hyprctl.get_option(SECTION, 'dim_inactive', 'int')))
        dimInactiveCheckBox.stateChanged.connect(lambda state: self.hyprctl.set_option(SECTION, 'dim_inactive', 'true' if state == 2 else 'false'))
        hLayout.addWidget(dimInactiveCheckBox)

        vLayout = QVBoxLayout()
        # Dim Strength
        dimStrengthLabel = QLabel("Dim strength (0.0 - 1.0)")
        dimStrengthSpin = QDoubleSpinBox()
        dimStrengthSpin.setRange(0.0, 1.0)
        dimStrengthSpin.setSingleStep(0.1)
        dimStrengthSpin.setValue(float(self.hyprctl.get_option(SECTION, 'dim_strength', 'float')))
        dimStrengthSpin.valueChanged.connect(lambda state: self.hyprctl.set_option(SECTION, 'dim_strength', 'true' if state == 2 else 'false'))
        vLayout.addWidget(dimStrengthLabel)
        vLayout.addWidget(dimStrengthSpin)
        
        hLayout.addLayout(vLayout)
        layout.addLayout(hLayout)

        # Dim Special
        dimSpecialLabel = QLabel("Dim special - how much to dim the rest of the screen by when a special workspace is open.")
        dimSpecialSlider = QSlider(Qt.Orientation.Horizontal)
        dimSpecialSlider.setRange(0, 100)
        dimSpecialSlider.setValue(int(self.hyprctl.get_option(SECTION, 'dim_secial', 'int')) * 100)
        dimSpecialSlider.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, 'dim_special', value / 100))
        layout.addWidget(dimSpecialLabel)
        layout.addWidget(dimSpecialSlider)

        # Dim Around
        dimAroundLabel = QLabel("Dim around - how much the dimaround window rule should dim by")
        dimAroundSlider = QSlider(Qt.Orientation.Horizontal)
        dimAroundSlider.setRange(0, 100)
        dimAroundSlider.setValue(int(float(self.hyprctl.get_option(SECTION, 'dim_around', 'float')) * 100))
        dimAroundSlider.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, 'dim_around', value / 100))
        layout.addWidget(dimAroundLabel)
        layout.addWidget(dimAroundSlider)


        return group




if __name__ == "__main__":
    app = QApplication([])
    window = AppearancePage()
    window.show()
    app.exec()
