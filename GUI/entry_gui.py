from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, \
    QComboBox, QHBoxLayout
from PySide6.QtCore import QTimer
from installer.utilities import show_notification
from installer.database import DatabasePSQL
from installer.crypto import Crypto

class NewEntry(QMainWindow):
    def __init__(self,db_connection:DatabasePSQL):
        super().__init__()

        self.i = 0
        self.db = db_connection

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
        self.b_send.clicked.connect(self.send)

        main_layout.addWidget(self.l_designation)
        main_layout.addWidget(self.lE_designation)

        main_layout.addWidget(self.l_type)
        main_layout.addWidget(self.dD_type)
        password_horizontal_layout.addWidget(self.lE_type_input)
        password_horizontal_layout.addWidget(self.b_showPassword)
        password_horizontal_layout.addWidget(self.b_randomize)
        main_layout.addLayout(password_horizontal_layout)

        main_layout.addWidget(self.b_send)

    def send(self):
        print("send")
        if self.checkFields():
            print("encrypting")
            crypto = Crypto(self.lE_type_input.text())
            key = self.db.retrieveKey()
            crypto.setKey(key)

            crypto.createCipherSuite()

            password_encrypted = crypto.encrypt()

            self.db.createEntryPWTable(password_encrypted)

            password_encrypted = self.db.retrievePassword()
            password_decrypted = crypto.decrypt(password_encrypted)
            print(password_decrypted.decode('utf-8'))


    def checkFields(self):
        print("checkFields")
        if not self.lE_designation.text():
            self.lE_designation.setPlaceholderText("Cannot be left blank!")
            show_notification("The designation has been left blank!")

            return False
        if self.dD_type.currentText() == "Auswahl":
            show_notification("No type has been chosen!")

            return False

        return True

    def showClearPassword(self):
        self.lE_type_input.setEchoMode(QLineEdit.Normal)
        QTimer.singleShot(2000, self.hidePassword)

    def hidePassword(self):
        # Revert to masked mode
        self.lE_type_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)

    def randomizePassword(self):
        self.lE_type_input.setText(f"TEST_{self.i}")
        self.i += 1