from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger


class LoginDialog(QDialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        logger.error_msg("__init__: Started LoginDialog.", None)

        username_label = QLabel("Username: ")
        if USERNAME is None:
            self.username = QLineEdit()
        else:
            self.username = QLineEdit(USERNAME)
        password_label = QLabel("Password: ")
        self.password = QLineEdit()
        self.username_check_box = QCheckBox("Remember username ")
        if USERNAME is not None:
            self.username_check_box.setChecked(True)
        self.password_check_box = QCheckBox("Remember password ")
        self.login_button = QPushButton("Login")
        self.cancel_button = QPushButton("Cancel")

        layout = QGridLayout()
        layout.addWidget(username_label, 0, 0)
        layout.addWidget(self.username, 0, 1)
        layout.addWidget(password_label, 1, 0)
        layout.addWidget(self.password, 1, 1)
        layout.addWidget(self.username_check_box, 2, 0, 1, 2)
        layout.addWidget(self.password_check_box, 3, 0, 1, 2)
        layout.addWidget(self.login_button, 4, 0)
        layout.addWidget(self.cancel_button, 4, 1)
        self.setLayout(layout)

        self.connect(self.login_button, SIGNAL("clicked()"), self.try_login)
        self.connect(self.cancel_button, SIGNAL("clicked()"), self, SLOT("reject()"))

        self.setWindowTitle("Login")

        logger.error_msg("__init__: Finished LoginDialog.", None)

    def try_login(self):
        logger.error_msg("try_login: Checking if given username and password are ok.", None)
        global USERNAME, PASSWORD
        if self.parent().try_login(str(self.username.text()), str(self.password.text())):
            logger.error_msg("try_login: Successful login.", None)
            if self.username_check_box.isChecked():
                USERNAME = self.username.text()
            if self.password_check_box.isChecked():
                PASSWORD = self.password.text()
            self.accept()
        else:
            logger.error_msg("try_login: Failed login.", None)
            self.password.clear()