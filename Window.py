from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QStackedWidget, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from src.pages.General import GeneralPage
from src.pages.Appearance import AppearancePage

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

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
                      }

                  QStackedWidget {
                      border-left: 1px solid #E9D7FE;
                      border-top: 1px solid #E9D7FE;
                      border-top-left-radius: 10px;
                      }
                  QSlide {
                      height: 100px;

                      }
                  QSlider::groove {
                      border: 1px solid #999;
                      height: 6px;
                      background: #999999;
                      margin: 0 12px;
                      }

                  QSlider::sub-page {
                      background: #9E77ED;
                      }

                  QSlider::add-page {
                      background: #999999;
                      }

                  QSlider::handle:horizontal {
                      background-color: #fff;
                      border-radius: 999px;
                      border: 2px solid #D6BBFB;
                      width: 15px;
                      height: 100px;
                      margin: -24px -12px;
                      }
                      """)
window = MainWindow()
window.show()
app.exec_()

