import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, \
    QComboBox, QMessageBox, QHBoxLayout
from PySide6.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.i = 0

        # Create the main widget and layout
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        password_horizontal_layout = QHBoxLayout()

        self.l_designation = QLabel("Enter designation:")
        self.lE_designation = QLineEdit()
        self.lE_designation.setPlaceholderText("default designation")

        self.l_type = QLabel("Chose a type:")
        self.dD_type = QComboBox(self)
        self.dD_type.addItems(["Auswahl", "Passwort", "Token"])
        self.dD_type.setCurrentIndex(0)

        self.lE_type_input = QLineEdit()
        self.lE_type_input.setPlaceholderText("default password/token")
        self.lE_type_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.b_showPassword = QPushButton("Show", self)
        self.b_showPassword.clicked.connect(self.showClearPassword)
        self.b_randomize = QPushButton("Randomize", self)
        self.b_randomize.clicked.connect(self.randomizePassword)

        self.b_send = QPushButton("Done", self)
        self.b_send.clicked.connect(self.checkFields)

        main_layout.addWidget(self.l_designation)
        main_layout.addWidget(self.lE_designation)

        main_layout.addWidget(self.l_type)
        main_layout.addWidget(self.dD_type)
        password_horizontal_layout.addWidget(self.lE_type_input)
        password_horizontal_layout.addWidget(self.b_showPassword)
        password_horizontal_layout.addWidget(self.b_randomize)
        main_layout.addLayout(password_horizontal_layout)

        main_layout.addWidget(self.b_send)

    def checkFields(self):
        if self.lE_designation.text() == "":
            self.lE_designation.setPlaceholderText("Cannot be left blank!")
            self.show_notification("The designation has been left blank!")
        if self.dD_type.currentText() == "Auswahl":
            self.show_notification("No type has been chosen!")

    def show_notification(self,text):
        # Create a QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(text)
        msg_box.setWindowTitle("Error!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def showClearPassword(self):
        self.lE_type_input.setEchoMode(QLineEdit.Normal)
        QTimer.singleShot(2000, self.hidePassword)

    def hidePassword(self):
        # Revert to masked mode
        self.lE_type_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)

    def randomizePassword(self):
        self.lE_type_input.setText(f"TEST_{self.i}")
        self.i += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
