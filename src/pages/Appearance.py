from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QHBoxLayout, QMainWindow, QSizePolicy, QSlider, QSpacerItem, QSpinBox, QVBoxLayout, QGroupBox, QLabel,  QWidget
from ..backend.hyprctl import HyprctlWrapper
from ..components.CToggleLabel import CToggleLabel
from ..components.CSlider import CSlider
from ..components.CSpinBoxLabel import CSpinBoxLabel


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

        self.mainLayout.addWidget(pageTitle)
        self.mainLayout.addWidget(self.appearanceGroup())
        self.mainLayout.addWidget(self.antialiasingAndOpacityGroup())
        self.mainLayout.addWidget(self.shadowGroup())
        self.mainLayout.addWidget(self.dimGroup())
        self.mainLayout.addWidget(self.blurGroup())

        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


    def appearanceGroup(self):
        group = QGroupBox("Appearance")
        layout = QVBoxLayout()

        # border size
        borderSizeBox = CSpinBoxLabel("Border size",
                                      SECTION,
                                      'border_size',
                                      "size of the border around windows"
                                      )
        layout.addWidget(borderSizeBox)



        

        # gaps in

        # gaps out

        # inactive border color

        # active border color

        # group border color
        
        # group border actie color

        # locked group border color

        #locked group border inactive color

        # curosr inactive timeout


        return group


    def antialiasingAndOpacityGroup(self):
        group = QGroupBox("Antialiasing and Opacity")
        layout = QVBoxLayout()

        # multisample_edges
        multisampleEdgesCheckbox = CToggleLabel("Enable antialiasing (no-jaggies) for rounded corners", SECTION, 'multisample_edges', 'int')
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

        # drop shadow
        dropShadowCheckBox = CToggleLabel("Enable drop shadow", SECTION, 'drop_shadow', 'int')
        layout.addWidget(dropShadowCheckBox)

        # window ignore
        shadowIgnoreCheckBox = CToggleLabel("Window ignore",
                                            SECTION,
                                            'shadow_ignore_window',
                                            'int',
                                            "(if true the shadow will not be rendered behind the window, only around it)")

        layout.addWidget(shadowIgnoreCheckBox)

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

    
    def blurGroup(self):
        group = QGroupBox("Blur")
        layout = QVBoxLayout()
        group.setLayout(layout)

        # Enable kawase blur
        kawaseBlur = CToggleLabel("Enable Kawase blur",
                                  SECTION,
                                  'blur:enabled',
                                  'int',
                                  "enable kawase window background blur")
        layout.addWidget(kawaseBlur)

        # blur size
        bhLayout = QHBoxLayout()
        blurSizeLabel = QLabel("Blur size (distance)")
        blurSizeSlider = CSlider()
        blurSizeSlider.setRange(0, 16)
        blurSizeSlider.setValue(int(self.hyprctl.get_option(SECTION, 'blur:size', 'int')))
        blurSizeSlider.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, 'blur:size', value))

        bhLayout.addWidget(blurSizeLabel)
        bhLayout.addWidget(blurSizeSlider)
        layout.addLayout(bhLayout)

        # passes
        bhpLayout = QHBoxLayout()
        blurPassesLabel = QLabel("Blur passes amount")
        blurPassesSlider = QSlider(Qt.Orientation.Horizontal)
        blurPassesSlider.setRange(0, 3)
        blurPassesSlider.setValue(int(self.hyprctl.get_option(SECTION, 'blur:passes', 'int')))
        blurPassesSlider.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, 'blur:passes', value))

        bhpLayout.addWidget(blurPassesLabel)
        bhpLayout.addWidget(blurPassesSlider)
        
        layout.addLayout(bhpLayout)

        # ignore opacity
        ignoreOpacity = CToggleLabel("Ignore opacity",
                                     SECTION,
                                     'blur:ignore_opacity',
                                     'int',
                                     "make the blur layer ignore the opacity of the window")
        layout.addWidget(ignoreOpacity)

        # new optimizations
        newOpt = CToggleLabel("New optimizations",
                              SECTION,
                              'blur:new_optimizations',
                              'int',
                              "whether to enable further optimizations to the blur. Recommended to leave on, as it will massively improve performance.")
        layout.addWidget(newOpt)

        # X ray
        xray = CToggleLabel("X-ray",
                            SECTION,
                            'blur:xray',
                            'int',
                            "if enabled, floating windows will ignore tiled windows in their blur. Only available if blur_new_optimizations is true. Will reduce overhead on floating blur significantly.")
        layout.addWidget(xray)
    
        return group


    def dimGroup(self):
        group = QGroupBox("Dim")
        layout = QVBoxLayout()
        group.setLayout(layout)


        hLayout = QHBoxLayout()
        # Dim Inactive
        dimInactiveCheckBox = CToggleLabel("Dim inactive windows", SECTION, 'dim_inactive', 'int')
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
