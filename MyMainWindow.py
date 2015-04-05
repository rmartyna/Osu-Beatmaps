from PyQt4.QtCore import *
from PyQt4.QtGui import *
from init import *
import connector
import logger
import BeatmapWidget
import LoginDialog
import LogoutDialog
import OptionsDialog
import AboutDialog
import ExitDialog
import images


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        logger.error_msg("__init__: Started MyMainWindow.", None)
        self.set_widget()
        logger.error_msg("__init__: Set main widget.", None)
        self.add_file_menu()
        logger.error_msg("__init__: Added file menu.", None)
        self.try_login(SETTINGS['USERNAME'], SETTINGS['PASSWORD'])
        logger.error_msg("__init__: Tried to login.", None)

        self.setWindowTitle("Osu Beatmaps!")
        self.setWindowIcon(images.get_icon())

        logger.error_msg("__init__: Finished MyMainWindow.", None)

    def set_widget(self):
        self.main_widget = QListWidget()
        self.items = []
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

        self.add_widget_action = self.menuBar().addAction("Add Widget")
        self.connect(self.add_widget_action, SIGNAL("triggered()"), self.add_widget)

        self.exit_action = self.menuBar().addAction("Exit")
        self.connect(self.exit_action, SIGNAL("triggered()"), self.pop_exit_dialog)

    def pop_login_dialog(self):
        logger.error_msg("pop_login_dialog: Started LoginDialog.", None)
        LoginDialog.LoginDialog(self).exec_()
        logger.error_msg("pop_login_dialog: Finished LoginDialog.", None)

    def pop_logout_dialog(self):
        logger.error_msg("pop_logout_dialog: Started LogoutDialog.", None)
        if LogoutDialog.LogoutDialog(self).exec_():
            logger.error_msg("pop_logout_dialog: LogoutDialog accepted.", None)
            SETTINGS['PASSWORD'] = None
            logger.error_msg("pop_logout_dialog: Resetting connection.", None)
            connector.reset_connection()
            logger.error_msg("pop_logout_dialog: Changing login/logout enabled flags.", None)
            self.logout_action.setEnabled(False)
            self.login_action.setEnabled(True)
        logger.error_msg("pop_logout_dialog: Started LogoutDialog.", None)

    def pop_options_dialog(self):
        logger.error_msg("pop_options_dialog: Started OptionsDialog.", None)
        options_dialog = OptionsDialog.OptionsDialog(self)
        if options_dialog.exec_():
            logger.error_msg("pop_options_dialog: OptionsDialog accepted.", None)
        logger.error_msg("pop_options_dialog: Finished OptionsDialog.", None)

    def pop_about_dialog(self):
        logger.error_msg("pop_about_dialog: Started AboutDialog.", None)
        AboutDialog.AboutDialog(self).exec_()
        logger.error_msg("pop_about_dialog: Finished AboutDialog.", None)

    def add_widget(self):
        logger.error_msg("add_widget: Adding widget.", None)
        item = QListWidgetItem()
        item.setSizeHint(QSize(100, 100))
        widget = BeatmapWidget.BeatmapWidget()
        self.items.append((item, widget))
        self.main_widget.addItem(item)
        self.main_widget.setItemWidget(item, widget)
        logger.error_msg("add_widget: Added widget.", None)

    def pop_exit_dialog(self):
        logger.error_msg("pop_exit_dialog: Started ExitDialog.", None)
        if ExitDialog.ExitDialog(self).exec_():
            logger.error_msg("pop_exit_dialog: ExitDialog accepted.", None)
            self.close()
        logger.error_msg("pop_exit_dialog: Finished ExitDialog.", None)

    def try_login(self, username, password):
        logger.error_msg("try_login: Started login.", None)
        if type(username) is not str or type(password) is not str:
            logger.error_msg("try_login: Username or password is not string.", None)
        else:
            logger.error_msg("try_login: Trying to login with given username and password.", None)
            connector.login(username, password)
        if connector.check_if_logged():
            logger.error_msg("try_login: Successfully connected.", None)
            self.login_action.setEnabled(False)
            self.logout_action.setEnabled(True)
            return True
        else:
            logger.error_msg("try_login: Could not login.", None)
            self.login_action.setEnabled(True)
            self.logout_action.setEnabled(False)
            return False