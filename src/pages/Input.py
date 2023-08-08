import json
import os

from PySide6.QtWidgets import QComboBox, QGroupBox, QMainWindow, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
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
        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    
    def keyboardGroup(self):
        group = QGroupBox("Keyboard")
        layout = QVBoxLayout()
        
        #Keyboard Layout
        self.keyboardLayout = QComboBox()
        self.keyboardLayout.addItems(self.LAYOUT_VARIANTS.keys())
        self.keyboardLayout.setCurrentText(str(self.hyprctl.get_option(SECTION, 'kb_layout', 'str')))
        self.keyboardLayout.currentIndexChanged.connect(self.onLayoutChange)
        layout.addWidget(self.keyboardLayout)

        # Keyboard variant
        self.keyboardVariant = QComboBox()
        self.keyboardVariant.addItems(self.LAYOUT_VARIANTS[self.keyboardLayout.currentText()])
        layout.addWidget(self.keyboardVariant) 
        

        group.setLayout(layout)
        return group

    
    def onLayoutChange(self, index):
        selectedLayout = self.keyboardLayout.itemText(index)
        self.onVariantChange(selectedLayout)
        self.hyprctl.set_option(SECTION, 'kb_layout', selectedLayout)
        self.onVariantChange(0)

    def onVariantChange(self, index):
        selectedVariant = self.keyboardVariant.itemText(index)
        self.hyprctl.set_option(SECTION, 'kb_variant', selectedVariant)

    
    def updateVariant(self, selectedLayout):
        self.keyboardVariant.clear()
        self.keyboardVariant.addItems(self.LAYOUT_VARIANTS[selectedLayout])

