from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QStackedWidget, QStyleFactory, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from src.pages.General import GeneralPage
from src.pages.Appearance import AppearancePage

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Hyprland Settings")

        self.sidebar = QListWidget()
        self.OPTIONS = ["General", "Appearance", "Animations", "Input", "Misc", "Binds", "Debug", "Monitor"]
        self.sidebar.addItems(self.OPTIONS)
        self.sidebar.setFixedWidth(self.width() // 4)
        self.sidebar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.sidebar.setStyleSheet("""
            QListWidget {
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

        self.mainArea = QStackedWidget()

        for option in self.OPTIONS:
            if option == "General":
                page = GeneralPage()
            elif option == "Appearance":
                page = AppearancePage()
            else:
                page = QWidget()
                layout = QVBoxLayout()
                page.setLayout(layout)
            self.mainArea.addWidget(page)
        self.sidebar.currentRowChanged.connect(self.mainArea.setCurrentIndex)

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.sidebar)
        self.hLayout.addWidget(self.mainArea)

        centralWidget = QWidget()
        centralWidget.setLayout(self.hLayout)
        self.setCentralWidget(centralWidget)

app = QApplication([])
app.setStyleSheet("""
                  * {
                      background-color: #f6f6f6;
                      font-family: "Segoe UI", sans-serif;
                      }

                  QGroupBox {
                      font-size: 14px;
                      font-weight: semi-bold;
                      }
                  """)
window = MainWindow()
window.show()
app.exec_()

