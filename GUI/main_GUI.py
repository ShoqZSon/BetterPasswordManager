import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from GUI.login_gui import Login
from GUI.entry_gui import NewEntry
from installer.database import DatabasePSQL

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.NewEntry = None

        self.pages = [Login(self), QWidget()] # QWidget() placeholder for the NewEntry() object
        self.current_page_index = 0

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)

        self.layout.addWidget(self.pages[self.current_page_index])
        self.setWindowTitle("Password Manager")

    def set_current_page(self, index, db_connection:DatabasePSQL):
        self.layout.itemAt(0).widget().setParent(None)  # Remove current page
        self.current_page_index = index
        if db_connection:
            self.pages[1] = NewEntry(db_connection)

        self.layout.addWidget(self.pages[self.current_page_index])  # Add new


if __name__ == "__main__":
    app = QApplication()

    main = MainWindow()
    main.show()

    sys.exit(app.exec())
