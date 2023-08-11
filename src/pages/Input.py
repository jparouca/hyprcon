import json
import os

from ..components.CToggleLabel import CToggleLabel
from PySide6.QtWidgets import QComboBox, QGroupBox, QLabel, QMainWindow, QSizePolicy, QSlider, QSpacerItem, QVBoxLayout, QWidget
from ..backend.hyprctl import HyprctlWrapper

LAYOUT_VARIANTS_PATH = os.path.abspath('src/assets/layouts.json')
SECTION = "input"


class InputPage(QMainWindow):
    def __init__(self, parent=None):
        super(InputPage, self).__init__(parent)
        self.hyprctl = HyprctlWrapper()

        with open(LAYOUT_VARIANTS_PATH, 'r') as f:
            self.LAYOUT_VARIANTS = json.load(f)

        mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(mainWidget)
        self.setCentralWidget(mainWidget)

        self.mainLayout.addWidget(self.keyboardGroup())
        self.mainLayout.addWidget(self.mouseGroup())
        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    
    def keyboardGroup(self):
        group = QGroupBox("Keyboard")
        layout = QVBoxLayout()
        
        #Keyboard Layout
        self.keyboardLayout = QComboBox()
        self.keyboardLayout.addItems(self.LAYOUT_VARIANTS.keys())
        self.keyboardLayout.setCurrentText(str(self.hyprctl.get_option(SECTION, 'kb_layout', 'str')))
        self.keyboardLayout.currentTextChanged.connect(self.onLayoutChange)
        layout.addWidget(self.keyboardLayout)

        # Keyboard variant
        self.keyboardVariant = QComboBox()
        self.keyboardVariant.addItems(self.LAYOUT_VARIANTS[self.keyboardLayout.currentText()])
        self.keyboardVariant.setCurrentText(str(self.hyprctl.get_option(SECTION, 'kb_variant', 'str')))
        self.keyboardVariant.currentTextChanged.connect(self.onVariantChange)
        layout.addWidget(self.keyboardVariant) 
        

        group.setLayout(layout)
        return group


    def mouseGroup(self):
        group = QGroupBox("Mouse")
        layout = QVBoxLayout()


        # group
        # force no accell
        noAccellCheck =  CToggleLabel("Force no acceleration", SECTION, 'force_no_accel', 'int')
        layout.addWidget(noAccellCheck)

        # Sensitivity
        layout.addWidget(QLabel("Mouse Sensitivity"))
        slider = QSlider()
        slider.setRange(0, 100)
        slider.setValue(self.hyprctl.get_option(SECTION, 'Sensitivity', 'float'))
        slider.valueChanged.connect(lambda value: self.hyprctl.set_option(SECTION, 'Sensitivity', value))
        layout.addWidget(slider)

        # Acell Profile
        acellCombo = QComboBox()
        acellCombo.addItems(['adaptive', 'flat'])
        acellCombo.setCurrentText(str(self.hyprctl.get_option(SECTION, 'accell_profile', 'str')))
        acellCombo.currentTextChanged.connect(lambda text: self.hyprctl.set_option(SECTION, 'accell_profile', text))
        layout.addWidget(acellCombo)


        group.setLayout(layout)



        return group

    
    def onLayoutChange(self):
        self.keyboardLayout.currentTextChanged.disconnect()
        selectedLayout = self.keyboardLayout.currentText()
        self.keyboardVariant.clear()
        self.keyboardVariant.addItems(self.LAYOUT_VARIANTS[selectedLayout])
        self.keyboardVariant.currentTextChanged.connect(self.onVariantChange)

    def onVariantChange(self):
        selectedLayout = self.keyboardLayout.currentText()
        selectedVariant = self.keyboardVariant.currentText()
        
        if selectedVariant:
            self.hyprctl.set_option(SECTION, 'kb_layout', selectedLayout)
            self.hyprctl.set_option(SECTION, 'kb_variant', selectedVariant)
