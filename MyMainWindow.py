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