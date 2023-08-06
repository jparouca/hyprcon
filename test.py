import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                QWidget, QLabel, QSlider, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("PySide6 Window")

        # Main layout
        main_layout = QVBoxLayout()

        self.desc_label = QLabel("Outside gap of windows")
        self.desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.desc_label)

        # Create a QHBoxLayout for the slider and its value label
        slider_layout = QHBoxLayout()

        # Create a spacer to push the slider and the label to the center
        slider_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(20)
        self.slider.setValue(self.get_option('general:gaps_out'))
        self.slider.valueChanged.connect(self.change_option)
        slider_layout.addWidget(self.slider)

        self.value_label = QLabel()
        self.value_label.setText(str(self.slider.value()))
        slider_layout.addWidget(self.value_label)

        # Another spacer to keep the slider and the label centered
        slider_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Add the slider layout to the main layout
        main_layout.addLayout(slider_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def get_option(self, option):
        # Run the command and get its output
        result = subprocess.run(['hyprctl', '-j', 'getoption', option], capture_output=True, text=True)

        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return int(data.get('int'))
            except json.JSONDecodeError:
                return 0
        else:
            return 0

    def change_option(self, value):
        # Update the value label
        self.value_label.setText(str(value))
        
        # Run the command to set the new value
        result = subprocess.run(['hyprctl', '--batch', f"keyword general:gaps_out {value}"], capture_output=True, text=True)
        if result.returncode != 0:
            # If there's an error, display a message box
            QMessageBox.critical(self, "Error", "Failed to set new value")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())

