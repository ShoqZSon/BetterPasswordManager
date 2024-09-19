import utilities as util
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTextEdit, QProgressBar
from PySide6.QtCore import QTimer
import validateLocation as VL
import validateUserInput as VU
import os

from setupDB import DatabasePSQL
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.progress = 0
        self.invalidChars_sql = ["'", '"', ';', '--', '/*', '*/', '(', ')', '=', '<', '>', '|', '~']

        self.invalidChars = ['<','>','"','?','°','`','´']
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        self.infoText = QTextEdit()
        self.infoText.setReadOnly(True)
        self.infoText.setText("Put in your desired path for the files of the password manager.\n"
                              "This will create a new folder with the necessary files inside the path."
                              "")

        self.l_install_path = QLabel("Enter the absolut installation path:")
        self.lE_install_path = QLineEdit()
        self.lE_install_path.setPlaceholderText("path/to/installation")

        self.l_install_folder = QLabel("Enter the name of the folder:")
        self.lE_install_folder = QLineEdit()
        self.lE_install_folder.setPlaceholderText("MyPasswortManager")

        self.l_username = QLabel("Enter your username:")
        self.tE_username = QTextEdit()
        self.tE_username.setReadOnly(True)
        self.tE_username.setText("Rules:"
                                 "Between 5 and 25 characters (inclusive)."
                                 f"Invalid chars: {self.invalidChars}.")
        self.lE_username = QLineEdit()
        self.lE_username.setPlaceholderText("username")

        self.l_password = QLabel("Enter your master password:")
        self.tE_password = QTextEdit()
        self.tE_password.setReadOnly(True)
        self.tE_password.setText("Rules:"
                                 "Between 10 and 30 characters (inclusive)."
                                 f"Invalid chars: {self.invalidChars}.")
        self.lE_password = QLineEdit()
        self.lE_password.setPlaceholderText("master password")
        self.lE_password.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.b_install = QPushButton("Install", self)
        self.b_install.clicked.connect(self.install)

        # Create a QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)  # Minimum value
        self.progress_bar.setMaximum(100)  # Maximum value
        self.progress_bar.setValue(0)  # Initial value

        main_layout.addWidget(self.infoText)
        main_layout.addWidget(self.l_install_path)
        main_layout.addWidget(self.lE_install_path)
        main_layout.addWidget(self.l_install_folder)
        main_layout.addWidget(self.lE_install_folder)
        main_layout.addWidget(self.l_username)
        main_layout.addWidget(self.lE_username)
        main_layout.addWidget(self.l_password)
        main_layout.addWidget(self.lE_password)
        main_layout.addWidget(self.b_install)
        main_layout.addWidget(self.progress_bar)


    def validation(self):
        if self.validateUserInput() and self.validatePath() and self.validateFolder():
            if self.validateUsername() and self.validatePassword():
                return True

        return False


    def validateUserInput(self) -> bool:
        if not self.lE_install_path.text():
            util.show_notification("The installation path is empty!")
            return False
        elif len(self.lE_install_path.text()) > VU.MAX_INPUT_LENGTH:
            util.show_notification("The installation path is too long!")
            return False
        elif VU.invalidChars(self.lE_install_path.text(), self.invalidChars_sql):
            util.show_notification("The installation path is invalid!")
            return False
        else:
            return True

    def validatePath(self) -> bool:
        if not os.path.exists(self.lE_install_path.text()):
            util.show_notification("The location does not exist!")
            return False
        elif not os.path.isdir(self.lE_install_path.text()):
            util.show_notification("The location is not a directory!")
            return False
        elif not os.access(self.lE_install_path.text(), os.W_OK):
            util.show_notification("The location is not writable!")
            return False
        elif VL.checkSpace(self.lE_install_path.text()):
            util.show_notification("The disk chosen for the installation is full!")
            return False
        else:
            return True

    def validateUsername(self):
        if not self.lE_username.text():
            util.show_notification("The username is empty!")
            return False
        elif len(self.lE_username.text()) < 5:
            util.show_notification("The username is too short!")
            return False
        elif len(self.lE_username.text()) > 25:
            util.show_notification("The username is too long!")
            return False
        elif any(char in self.invalidChars for char in self.lE_username.text()):
            util.show_notification("The username is invalid!")
            return False
        else:
            return True

    def validatePassword(self):
        if not self.lE_password.text():
            util.show_notification("The password is empty!")
            return False
        elif len(self.lE_password.text()) < 10:
            util.show_notification("The password is too short!")
            return False
        elif len(self.lE_username.text()) > 30:
            util.show_notification("The password is too long!")
            return False
        elif any(char in self.invalidChars for char in self.lE_username.text()):
            util.show_notification("The password is invalid!")
            return False
        else:
            return True

    def validateFolder(self) -> bool:
        folderPath = os.path.join(self.lE_install_path.text(), self.lE_install_folder.text())
        if os.path.exists(folderPath):
            util.show_notification("The folder already exists. Choose a different one!")
            return False

        return True


    def install(self) -> None:
        if self.validation():
            self.start_progress()
            # creates the base folder for the application files
            directory = util.createFolder(self.lE_install_path.text(), self.lE_install_folder.text())

            user_db = 'pwm_' + self.lE_username.text()
            db = DatabasePSQL(self.lE_username.text(),self.lE_password.text(),user_db)

            db.connect(db.get_admin_dbname(),db.get_admin_user(),db.get_admin_password())

            db.createDB()

            db.createUser()

            db.connect(user_db,self.lE_username.text(),self.lE_password.text())

            db.createPasswordsTable()

            db.disconnect()

            self.close()

    def start_progress(self):
        self.progress = 0
        self.progress_bar.setValue(self.progress)

    def update_progress(self):
        self.progress_bar.setValue(self.progress)
        QTimer.singleShot(1000, lambda: None)  # Non-blocking delay


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec())

