import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from GUI.login_gui import Login
from GUI.entry_gui import NewEntry


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.pages = [Login(self), NewEntry()]
        self.current_page_index = 0

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)

        self.layout.addWidget(self.pages[self.current_page_index])
        self.setWindowTitle("Password Manager")

    def set_current_page(self, index):
        self.layout.itemAt(0).widget().setParent(None)  # Remove current page
        self.current_page_index = index
        self.layout.addWidget(self.pages[self.current_page_index])  # Add new page

if __name__ == "__main__":
    app = QApplication()

    main = MainWindow()
    main.show()

    sys.exit(app.exec())
