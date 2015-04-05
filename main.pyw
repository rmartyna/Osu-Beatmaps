import sys
import pickle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from init import *
import connector
import logger


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        logger.error_msg("__init__: Making MainWindow.", None)
        self.load_settings()
        logger.error_msg("__init__: Loaded settings.", None)
        self.set_widget()
        logger.error_msg("__init__: Set main widget.", None)
        self.add_file_menu()
        logger.error_msg("__init__: Added file menu.", None)
        self.try_login(USERNAME, PASSWORD)
        logger.error_msg("__init__: Tried to login.", None)

        self.setWindowTitle("Osu Beatmaps!")

    def set_widget(self):
        self.main_widget = MyMainWidget()
        self.main_widget.setMinimumSize(800, 450)
        self.setCentralWidget(self.main_widget)



    def add_file_menu(self):
        self.login_action = self.menuBar().addAction("Login")
        self.connect(self.login_action, SIGNAL("triggered()"), self.pop_login_dialog)

        self.logout_action = self.menuBar().addAction("Logout")
        self.connect(self.logout_action, SIGNAL("triggered()"), self.pop_logout_dialog)

        self.options_action = self.menuBar().addAction("Options")
        self.connect(self.options_action, SIGNAL("triggered()"), self.pop_options_dialog)

        self.about_action = self.menuBar().addAction("About")
        self.connect(self.about_action, SIGNAL("triggered()"), self.pop_about_dialog)

        self.exit_action = self.menuBar().addAction("Exit")
        self.connect(self.exit_action, SIGNAL("triggered()"), self.pop_exit_dialog)

    def pop_login_dialog(self):
        LoginDialog(self).exec_()

    def pop_logout_dialog(self):
        global PASSWORD
        if LogoutDialog(self).exec_():
            PASSWORD = None
            connector.reset_connection()
            self.logout_action.setEnabled(False)
            self.login_action.setEnabled(True)

    def pop_options_dialog(self):
        options_dialog = OptionsDialog(self)
        if options_dialog.exec_():
            print("accepted")

    def pop_about_dialog(self):
        AboutDialog(self).exec_()

    def pop_exit_dialog(self):
        ExitDialog(self).exec_()

    def try_login(self, username, password):
        print(type(username))
        print(type(password))
        if type(username) is not str or type(password) is not str:
            pass
        else:
            connector.login(username, password)
        if connector.check_if_logged():
            self.login_action.setEnabled(False)
            self.logout_action.setEnabled(True)
            print("logged")
            return True
        else:
            self.login_action.setEnabled(True)
            self.logout_action.setEnabled(False)
            return False


def load_settings(self):
    global USERNAME, PASSWORD, DOWNLOAD_FOLDER, SETTINGS
    try:
        SETTINGS = pickle.load(open("config.dat", "rb"))
    except IOError:
        SETTINGS = dict()

    try:
        USERNAME = SETTINGS["username"]
    except KeyError:
        pass
    try:
        PASSWORD = SETTINGS["password"]
    except KeyError:
        pass
    try:
        DOWNLOAD_FOLDER = SETTINGS["download_folder"]
    except KeyError:
        pass

def save_settings(self):
    try:
        pickle.dump(SETTINGS, open("config.dat", "wb"))
        logger.error_msg("Saved settings.", None)
    except Exception as err:
        logger.error_msg("save_settings: Could not save settings.", err)


class MyMainWidget(QWidget):

    def __init__(self, parent=None):
        super(MyMainWidget, self).__init__(parent)

        self.add_buttons()

    def add_buttons(self):
        self.layout = QVBoxLayout()

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.label1 = QLabel()
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)


class LoginDialog(QDialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

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

    def try_login(self):
        global USERNAME, PASSWORD
        if self.parent().try_login(str(self.username.text()), str(self.password.text())):
            if self.username_check_box.isChecked():
                USERNAME = self.username.text()
            if self.password_check_box.isChecked():
                PASSWORD = self.password.text()
            self.accept()
        else:
            self.password.clear()


class LogoutDialog(QDialog):

    def __init__(self, parent=None):
        super(LogoutDialog, self).__init__(parent)

        label = QLabel("Are you sure you want to logout?")
        self.yesButton = QPushButton("Yes")
        self.noButton = QPushButton("No")

        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.yesButton, 1, 0)
        layout.addWidget(self.noButton, 1, 1)
        self.setLayout(layout)

        self.connect(self.yesButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.noButton, SIGNAL("clicked()"), self, SLOT("reject()"))

        self.setWindowTitle("Logout")



class OptionsDialog(QDialog):

    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)




class AboutDialog(QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        label = QLabel("""<b>Osu Beatmaps!</b> v. {0}
        <p>Last updated: {1}</p>
        <p>This application is used to help filter
        beatmaps,<br/>allowing you to download high quality
        maps automatically.</p>
        <p>You can contact me at: {2}</p>
        <p>More information and source code at:<br/>
         {3}</p>""".format(VERSION, DATE,
                                   EMAIL, GITHUB), self)
        self.button = QPushButton("OK")
        self.button.setMaximumWidth(100)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.button, 0, Qt.AlignCenter)
        self.setLayout(layout)

        self.connect(self.button, SIGNAL("clicked()"), self, SLOT("accept()"))

        self.setWindowTitle("About")

def main():
    load_settings()

    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    app.exec_()

    save_settings()

if __name__ == "__main__":
    main()