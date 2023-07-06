from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QSplitter, QLabel, QStackedWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Hyprland Settings")

        # Create a QSplitter widget
        splitter = QSplitter(Qt.Horizontal)

        # Create a QListWidget for the sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItems(["General", "Decoration", "Animations", "Input", "Etc."])
        self.sidebar.setFixedWidth(self.width() // 4)

        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: rgba(255, 255, 255, 127);
                color: black;
                padding: 10px;
                font-size: 16px;
            }

            QListWidget::item {
                min-height: 36px;
                padding: 6px;
                margin: 4px 2px;
                border-radius: 4px;
            }

            QListWidget::item:selected {
                background-color: rgba(0, 0, 0, 127);
                color: white;
            }
        """)

        # Add the sidebar to the splitter
        splitter.addWidget(self.sidebar)

        # Create a QStackedWidget for the main area
        self.main_area = QStackedWidget()
        for i in range(5):  # Assuming 5 options in QListWidget
            # Add a QLabel as a placeholder for each page
            # You could add any widget (or layout of widgets) you want
            label = QLabel(f"Content for option {i + 1}")
            self.main_area.addWidget(label)

        # Connect the currentRowChanged signal to a slot that changes the current widget in the QStackedWidget
        self.sidebar.currentRowChanged.connect(self.main_area.setCurrentIndex)

        # Add the main area to the splitter
        splitter.addWidget(self.main_area)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        # Set the splitter as the central widget
        self.setCentralWidget(splitter)


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

