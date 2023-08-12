import subprocess
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QLabel, QListWidgetItem, QMainWindow, QListWidget, QScrollArea, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from src.pages.General import GeneralPage
from src.pages.Appearance import AppearancePage
from src.pages.Input import InputPage


generalIcon = QIcon("./src/assets/cog-outline.svg")
appearanceIcon = QIcon("./src/assets/brush-outline.svg")
inputIcon = QIcon("./src/assets/keypad-outline.svg")
debugIcon = QIcon("./src/assets/bug-outline.svg")
monitorIcon = QIcon("./src/assets/desktop-outline.svg")


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setFixedSize(1200, 900)


        self.setWindowTitle("hyprcon")
        self.sidebar = QListWidget()
        self.OPTIONS = [("General", generalIcon), ("Appearance", appearanceIcon), ("Input", inputIcon) , ("Debug", debugIcon), ("Monitor", monitorIcon)]
        for OPTION, icon in self.OPTIONS:
            items = QListWidgetItem(icon, OPTION)
            self.sidebar.addItem(items)
        self.sidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.mainArea = QStackedWidget()
        for option, _ in self.OPTIONS:
            if option == "General":
                page = GeneralPage()
            elif option == "Appearance":
                page = AppearancePage()
            elif option == "Input":
                page = InputPage()
            else:
                page = QWidget()
                layout = QVBoxLayout()
                page.setLayout(layout)
            self.mainArea.addWidget(page)
        self.sidebar.currentRowChanged.connect(self.mainArea.setCurrentIndex)


        scrollArea = QScrollArea()
        scrollArea.setWidget(self.mainArea)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.sidebar, 1)
        self.hLayout.addWidget(scrollArea, 7)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.mainArea.setSizePolicy(sizePolicy)


        centralWidget = QWidget()
        centralWidget.setLayout(self.hLayout)
        self.setCentralWidget(centralWidget)

    def showEvent(self, event):
        super().showEvent(event)

        def toggleFloating():
            subprocess.run(["hyprctl", "dispatch", "togglefloating", "python3"])
            subprocess.run(["hyprctl", "dispatch", "centerwindow"])
            print("floating")
        QTimer.singleShot(500, toggleFloating)


app = QApplication([])
app.setStyleSheet("""
                  * {
                      background: #1A1A2E;
                      font-family: "Segoe UI", sans-serif;
                      color: #CFE8F6;
                      }

                  QGroupBox {
                      font-size: 16px;
                      font-weight: bold;
                      font-weight: 600;
                      }
                  QListWidget {
                      border: none;
                      font-weight: semi-bold;
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
                      font-size: 14px;
                      border: none;
                      }

                  QListWidget::item:hover {
                      background-color: #A6DADF;
                      border: none;
                      font-size: 15px;
                      color: #000;

                }
                  QListWidget::item:selected {
                      border: none;
                      background-color: #7FFFD4;
                      color: black;
                      font-size: 16px;

                      }
                  QStackedWidget {
                      border-top: 1px solid #B3B8DB;
                      border-top-left-radius: 10px;
                      }
                  QSlider::groove:horizontal {
                          border-radius: 5px;
                          height: 10px;
                          margin: 0px;
                          background-color: #1A1A2e;
                          }
                  QSlider::groove:horizontal:hover {
                          }

                    QSlider:handle:horizontal {
                            background-color: #fff;
                            border: none;
                            height: 15px;
                            width: 15px;
                            margin: 0px;
                            border-radius: 5px;
                            }
                    QSlider:handle:horizontal:hover {
                            }

                  QSlider::sub-page {
                      background: #7FFFD4;
                      }

                  QSlider::add-page {
                      background: #999999;
                      }

                  QCheckBox {
                          border: 1px solid #1A1A2E;
                          }

                  """)
window = MainWindow()
window.show()
app.exec_()

