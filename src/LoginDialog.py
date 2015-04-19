from PyQt4.QtGui import *
from PyQt4.QtCore import *
from init import *
import logger
import images


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        logger.error_msg("__init__: Started LoginDialog.", None)

        username_label = QLabel("Username: ")
        if SETTINGS['USERNAME'] is None:
            self.username = QLineEdit()
        else:
            self.username = QLineEdit(SETTINGS['USERNAME'])
        password_label = QLabel("Password: ")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.username_check_box = QCheckBox("Remember username ")
        self.password_check_box = QCheckBox("Remember password ")
        if SETTINGS['USERNAME'] is not None:
            self.username_check_box.setChecked(True)
        else:
            self.password_check_box.setEnabled(False)
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
        self.connect(self.username_check_box, SIGNAL("stateChanged(int)"), self.username_check_box_changed)
        self.connect(self.password_check_box, SIGNAL("stateChanged(int)"), self.password_check_box_changed)

        self.setWindowTitle("Login")
        self.setWindowIcon(images.get_icon())

        logger.error_msg("__init__: Finished LoginDialog.", None)

    def try_login(self):
        logger.error_msg("try_login: Checking if given username and password are ok.", None)
        if self.parent().try_login(str(self.username.text()), str(self.password.text())):
            logger.error_msg("try_login: Successful login.", None)
            if self.username_check_box.isChecked():
                logger.error_msg("try_login: Remember username is checked.", None)
                SETTINGS['USERNAME'] = str(self.username.text())
            else:
                logger.error_msg("try_login: Remember username is not checked.", None)
                SETTINGS['USERNAME'] = None
            if self.password_check_box.isChecked():
                logger.error_msg("try_login: Remember password is checked.", None)
                SETTINGS['PASSWORD'] = str(self.password.text())
            else:
                logger.error_msg("try_login: Remember password is not checked.", None)
                SETTINGS['PASSWORD'] = None
            self.accept()
        else:
            logger.error_msg("try_login: Failed login.", None)
            self.login_failed()
            self.password.clear()

    def username_check_box_changed(self, value):
        if value == 0:
            self.password_check_box.setEnabled(False)
        if value == 2:
            self.password_check_box.setEnabled(True)

    def password_check_box_changed(self, value):
        if value == 0:
            self.username_check_box.setEnabled(True)
        if value == 2:
            self.username_check_box.setEnabled(False)

    def login_failed(self):
        self.password.clear()
        QMessageBox.information(self, "Login failed", "Invalid username or password.")