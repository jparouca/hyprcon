from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QLabel, QListWidgetItem, QMainWindow, QListWidget, QStackedWidget, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
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

        self.sidebar = QListWidget()
        self.OPTIONS = [("General", generalIcon), ("Appearance", appearanceIcon), ("Input", inputIcon) , ("Debug", debugIcon), ("Monitor", monitorIcon)]
        for OPTION, icon in self.OPTIONS:
            items = QListWidgetItem(icon, OPTION)
            self.sidebar.addItem(items)
        self.sidebar.setFixedWidth(self.width() // 4)
        self.sidebar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

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
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.sidebar)
        self.hLayout.addWidget(self.mainArea)

        centralWidget = QWidget()
        centralWidget.setLayout(self.hLayout)
        self.setCentralWidget(centralWidget)

app = QApplication([])
app.setStyleSheet("""
                  * {
                      background: #fff;
                    
                      font-family: "Segoe UI", sans-serif;
                      }

                  QGroupBox {
                      font-size: 14px;
                      font-weight: semi-bold;
                      }
                  QListWidget {
                      border: none;
                      font-weight: semi-bold;
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
                      font-size: 14px;
                      border: none;
                      }

                  QListWidget::item:hover {
                      background-color: #D5D9EB;
                      border: none;
                      font-size: 15px;

                }
                  QListWidget::item:selected {
                      border: none;
                      background-color: #B3B8DB;
                      color: black;
                      font-size: 16px;

                      }
                  QStackedWidget {
                      border-left: 1px solid #B3B8DB;
                      border-top: 1px solid #B3B8DB;
                      border-top-left-radius: 10px;
                      }
                  QSlide {
                      height: 100px;
                      border-radius: 18px;

                      }
                  QSlider::groove {
                      border: 1px solid #999;
                      height: 6px;
                      background: #999999;
                        border-radius: 18px;
                      margin: 0 12px;
                      }

                  QSlider::sub-page {
                      background: #717BBC;
                      }

                  QSlider::add-page {
                      background: #999999;
                      }

                  QSlider::handle:horizontal {
                      background-color: #fff;
                      border-radius: 999px;
                      border: 2px solid #717BBC;
                      width: 15px;
                      height: 100px;
                      margin: -24px -12px;
                      }
                  """)
window = MainWindow()
window.show()
app.exec_()

