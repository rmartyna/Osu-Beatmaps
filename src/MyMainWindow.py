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
import scraper
import evaluator
import time
import threading


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
        self.main_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.items = []
        self.items_len = 0
        self.beatmaps = []
        self.beatmaps_to_add = []
        self.main_widget.setMinimumSize(800, 450)
        self.main_widget.setMaximumWidth(800)
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

        self.download_action = self.menuBar().addAction("Download")
        self.connect(self.download_action, SIGNAL("triggered()"), self.download_and_show_wrapper)
        self.connect(self, SIGNAL("add_widgets()"), self.add_widgets)
        self.connect(self, SIGNAL("copy_widget()"), self.copy_widget)

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

    def add_widget(self, beatmap):
        item = QListWidgetItem()
        item.setSizeHint(QSize(100, 100))
        widget = BeatmapWidget.BeatmapWidget(beatmap, item, self)
        self.main_widget.addItem(item)
        self.main_widget.setItemWidget(item, widget)
        self.items_len += 1

    def delete_widget(self, widget):
        current_index = self.main_widget.indexFromItem(widget).row()
        self.main_widget.takeItem(current_index)
        self.items_len -= 1

    def download_and_show_wrapper(self):
        thread = threading.Thread(target=MyMainWindow.download_and_show, args=(self,))
        thread.setDaemon(True)
        thread.start()
        thread = threading.Thread(target=MyMainWindow.copy_widgets_deamon, args=(self,))
        thread.setDaemon(True)
        thread.start()

    def download_and_show(self):
        logger.error_msg("download_and_show: Start of function.", None)
        if not connector.check_if_logged():
            QMessageBox.information(self, "Not logged in", "You should login first")
            return

        for page in range(1, 126):
            time.sleep(0.1)
            while True:
                if self.check_for_new_maps():
                    break
                else:
                    time.sleep(2)
            while self.beatmaps:
                self.beatmaps.pop()
            scraper.scrape_data(self.beatmaps, page)
            logger.error_msg("download_and_show: Finished scraping.", None)
            evaluator.filter(self.beatmaps)
            logger.error_msg("download_and_show: Finished evaluating.", None)
            scraper.scrape_data_after_filtering(self.beatmaps)
            logger.error_msg("download_and_show: Finished scraping after filtering.", None)
            self.emit(SIGNAL("add_widgets()"))
            logger.error_msg("download_and_show: Finished making widgets.", None)

    def add_widgets(self):
        for beatmap in self.beatmaps:
            self.beatmaps_to_add.append(beatmap)

    def copy_widgets_deamon(self):
        while True:
            if self.check_for_add_widget() and len(self.beatmaps_to_add) > 0:
                self.emit(SIGNAL("copy_widget()"))
                time.sleep(0.01)
            else:
                time.sleep(0.1)

    def copy_widget(self):
        self.add_widget(self.beatmaps_to_add.pop(0))

    def check_for_new_maps(self):
        return len(self.beatmaps_to_add) < 10

    def check_for_add_widget(self):
        return self.items_len < 10

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


class PageAction(QWidgetAction):
    def __init__(self, parent=None):
        super(PageAction, self).__init__(parent)

        self.widget = QWidget()
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Page: "), 0, 0, 1, 2)
        self.pageEdit = QLineEdit("1")
        self.layout.addWidget(self.pageEdit, 0, 2, 1, 1)
        self.pageEdit.setMaximumSize(45,20)
        self.widget.setLayout(self.layout)
        self.setDefaultWidget(self.widget)

    def page(self):
        return self.pageEdit.text()