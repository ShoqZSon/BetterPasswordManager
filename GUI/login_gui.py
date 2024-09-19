from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
from PySide6.QtCore import Qt
from installer.database import DatabasePSQL
from installer.utilities import show_notification

class Login(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        widget = QWidget()
        self.main_layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        self.l_header = QLabel('Password Manager')
        self.l_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l_header.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.l_username = QLabel('Enter your username')
        self.l_username.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lE_username = QLineEdit()
        self.lE_username.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lE_username.setPlaceholderText('myUsername')

        self.l_password = QLabel('Enter your password')
        self.l_password.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lE_password = QLineEdit()
        self.lE_password.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lE_password.setPlaceholderText('myPassword')

        self.b_login = QPushButton('Login')
        self.b_login.clicked.connect(self.login)

        self.main_layout.addWidget(self.l_header)
        self.main_layout.addWidget(self.l_username)
        self.main_layout.addWidget(self.lE_username)
        self.main_layout.addWidget(self.l_password)
        self.main_layout.addWidget(self.lE_password)

        self.main_layout.addWidget(self.b_login)

    def login(self):
        user_db = 'pwm_' + self.lE_username.text()
        db = DatabasePSQL(self.lE_username.text(), self.lE_password.text(),user_db)
        connected = db.connect(db.get_new_db(),db.get_new_user(),db.get_new_password())
        if connected:
            show_notification("Successfully logged in!")
            self.main_window.set_current_page(1,db)
        else:
            show_notification("Invalid username or password!")