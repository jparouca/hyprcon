from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QWidget, QLabel, QSlider, QComboBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
import sys
from ..backend.hyprctl import HyprctlWrapper


SECTION = "general"

class GeneralPage(QMainWindow):
    def __init__(self):
        super(GeneralPage, self).__init__()
        self.hyprctl = HyprctlWrapper()

        central_widget = QWidget()
        self.mainLayout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.mainLayout.addWidget(self.borderSizeComponent())
        self.mainLayout.addWidget(self.noBorderFloatingComponent())


    def borderSizeComponent(self):
        container = QWidget()
        layout = QHBoxLayout(container)

        title  = QLabel("Border size")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(self.hyprctl.get_option("border_size"))
        slider.setRange(0, 25)
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

        title = QLabel("No border on floating")
        combo = QComboBox()

        combo.addItem("true")
        combo.addItem("false")
        
        if self.hyprctl.get_option("no_border_floating") == 0:
            combo.setCurrentIndex(1) #false
        else:
            combo.setCurrentIndex(0)

        combo.currentTextChanged.connect(lambda: self.hyprctl.set_option(SECTION, "no_border_on_floating",  combo.currentText()))






        layout.addWidget(title)
        layout.addWidget(combo)

        return container



    def onSliderChange(self, sliderValue, option, value):
        print(self.hyprctl.get_option(option))
        sliderValue.setText(str(value))
        self.hyprctl.set_option(SECTION, option, value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hyprctl = HyprctlWrapper()
    window = GeneralPage()
    window.show()
    sys.exit(app.exec())
