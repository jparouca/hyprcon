from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QGraphicsBlurEffect, QMainWindow, QListWidget, QStackedWidget, QVBoxLayout, QWidget, QSplitter, QLabel
from PySide6.QtCore import Qt
from general import GeneralPage



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Hyprland Settings")

        splitter = QSplitter(Qt.Horizontal)

        self.sidebar = QListWidget()
        self.OPTIONS = ["General", "Decoration", "Animations", "Input", "Misc", "Binds", "Debug", "Monitor", "Option 9", "Option 10"]
        self.sidebar.addItems(self.OPTIONS)
        self.sidebar.setFixedWidth(self.width() // 4)
        self.sidebar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: rgba(249, 247, 245, 127);
                color: black;
                padding: 10px;
                font-size: 16px;
                outline: 0px;
                text-align: center;
            }

            QListWidget::item {
                min-height: 36px;
                padding: 6px;
                margin: 4px 2px;
                border-radius: 4px;
                border: none;
            }

            QListWidget::item:hover {
                background-color: rgba(236, 236, 236, 255);
                border: none;

            }
            QListWidget::item:selected {
                border: none;
                background-color: rgba(225, 225, 225, 255);
                color: black;
            }
        """)
        splitter.addWidget(self.sidebar)


    
        self.main_area = QStackedWidget()
        for option in self.OPTIONS:
            if option == "General":
                page = GeneralPage()
            else:
                page = QWidget()
                layout = QVBoxLayout()
                label = QLabel(option)
                layout.addWidget(label)
                page.setLayout(layout)
            self.main_area.addWidget(page)
        self.sidebar.currentRowChanged.connect(self.main_area.setCurrentIndex)

        splitter.addWidget(self.main_area)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

