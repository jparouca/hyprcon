from PySide6.QtWidgets import QApplication, QVBoxLayout, QGroupBox, QLabel, QSpinBox, QWidget, QScrollArea, QDoubleSpinBox, QCheckBox, QLineEdit, QColorDialog, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

class MySpinBox(QSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class MyDoubleSpinBox(QDoubleSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class MyCheckBox(QCheckBox):
    def wheelEvent(self, event):
        event.ignore()

class MyLineEdit(QLineEdit):
    def wheelEvent(self, event):
        event.ignore()

class GeneralPage(QWidget):
    def __init__(self, parent=None):
        super(GeneralPage, self).__init__(parent)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)

        # Create group boxes for different settings
        mouse_group = self.create_group("Mouse", [("sensitivity", MyDoubleSpinBox, 1.0)])
        border_group = self.create_group("Border", [("border_size", MySpinBox, 1), ("no_border_on_floating", MyCheckBox, False)])
        gaps_group = self.create_group("Gaps", [("gaps_in", MySpinBox, 5), ("gaps_out", MySpinBox, 20)])
        color_group = self.create_group("Color", [("col.inactive_border", QPushButton, QColor("white")), ("col.active_border", QPushButton, QColor("black"))])
        cursor_group = self.create_group("Cursor", [("cursor_inactive_timeout", MySpinBox, 0)])
        layout_group = self.create_group("Layout", [("layout", MyLineEdit, "dwindle")])

        # Add the group boxes to the main layout
        self.mainLayout.addWidget(mouse_group)
        self.mainLayout.addWidget(border_group)
        self.mainLayout.addWidget(gaps_group)
        self.mainLayout.addWidget(color_group)
        self.mainLayout.addWidget(cursor_group)
        self.mainLayout.addWidget(layout_group)

        self.scrollArea.setWidget(self.mainWidget)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scrollArea)

    def create_group(self, title, settings):
        group = QGroupBox(title)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 25, 0, 0)  # Add a margin of 25 pixels between the group box title and the rest of the content
        group.setLayout(layout)

        for setting in settings:
            label_text, widget_class, default_value = setting
            label = QLabel(label_text)
            widget = widget_class()
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.setValue(default_value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(default_value)
            elif isinstance(widget, QPushButton):
                widget.setFixedSize(100, 40)  # Make the button bigger
                widget.clicked.connect(lambda: self.open_color_dialog(widget))
                widget.setStyleSheet(f"background-color: {default_value.name()};")
            hbox = QHBoxLayout()
            hbox.addWidget(label)
            hbox.addWidget(widget)
            layout.addLayout(hbox)

        return group

    def open_color_dialog(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")

if __name__ == "__main__":
    app = QApplication([])
    window = GeneralPage()
    window.show()
    app.setStyleSheet("""
        * {
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
        }
        QGroupBox {
            font-size: 24px;
            font-weight: bold;
            margin-top: 2ex;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 0px 0 0px;
        }
        QLabel {
            padding: 5px;
        }
        QSpinBox, QDoubleSpinBox, QLineEdit, QPushButton {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        QCheckBox {
            padding: 5px;
        }
    """)
    app.exec()

