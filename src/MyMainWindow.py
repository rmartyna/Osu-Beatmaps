import time
import threading
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


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        logger.error_msg("__init__: Started MyMainWindow.", None)

        self.main_widget = QListWidget()
        self.main_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.items = []
        self.items_len = 0
        self.beatmaps = []
        self.beatmaps_to_add = []
        self.main_widget.setMinimumSize(800, 450)
        self.main_widget.setMaximumWidth(800)
        self.setCentralWidget(self.main_widget)

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
        self.exit_action = self.menuBar().addAction("Exit")
        self.connect(self.exit_action, SIGNAL("triggered()"), self.pop_exit_dialog)

        self.connect(self, SIGNAL("add_widgets_to_copy()"), self.add_widgets_to_copy)
        self.connect(self, SIGNAL("copy_widget()"), self.copy_widget)

        self.try_login(SETTINGS['USERNAME'], SETTINGS['PASSWORD'])

        self.setWindowTitle("Osu Beatmaps!")
        self.setWindowIcon(images.get_icon())

    def pop_login_dialog(self):
        LoginDialog.LoginDialog(self).exec_()

    def pop_logout_dialog(self):
        if LogoutDialog.LogoutDialog(self).exec_():
            SETTINGS['PASSWORD'] = None
            connector.reset_connection()
            self.logout_action.setEnabled(False)
            self.login_action.setEnabled(True)

    def pop_options_dialog(self):
        options_dialog = OptionsDialog.OptionsDialog(self)
        if options_dialog.exec_():
            SETTINGS['MIN_FAVOURITED'] = int(options_dialog.min_favourited_lineedit.text())
            SETTINGS['MIN_DIFFICULTY'] = float(options_dialog.min_difficulty_lineedit.text())
            SETTINGS['MIN_RANKED'] = int(options_dialog.min_ranked_lineedit.text())
            SETTINGS['MIN_NON_RANKED'] = int(options_dialog.min_non_ranked_lineedit.text())
            SETTINGS['MIN_PP_RANK'] = int(options_dialog.min_pp_rank_lineedit.text())

    def pop_about_dialog(self):
        AboutDialog.AboutDialog(self).exec_()

    def add_widget(self, beatmap):
        item = QListWidgetItem()
        item.setSizeHint(QSize(450, 120))
        widget = BeatmapWidget.BeatmapWidget(beatmap, item, self)
        self.main_widget.addItem(item)
        self.main_widget.setItemWidget(item, widget)
        self.items_len += 1

    def delete_widget(self, widget):
        current_index = self.main_widget.indexFromItem(widget).row()
        self.main_widget.takeItem(current_index)
        self.items_len -= 1

    def download_and_show_wrapper(self):
        if not connector.check_if_logged():
            QMessageBox.information(self, "Not logged in", "You should login first.")
            return
        thread = threading.Thread(target=MyMainWindow.downloader_daemon, args=(self,))
        thread.setDaemon(True)
        thread.start()
        thread = threading.Thread(target=MyMainWindow.copy_widgets_daemon, args=(self,))
        thread.setDaemon(True)
        thread.start()

    def downloader_daemon(self):
        logger.error_msg("downloader_daemon: Start of function.", None)


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
            evaluator.filter_maps(self.beatmaps)
            scraper.scrape_data_after_filtering(self.beatmaps)
            self.emit(SIGNAL("add_widgets_to_copy()"))

    def add_widgets_to_copy(self):
        for beatmap in self.beatmaps:
            self.beatmaps_to_add.append(beatmap)

    def copy_widgets_daemon(self):
        logger.error_msg("copy_widgets_daemon: Start of function.", None)
        while True:
            if self.check_if_add_widget() and len(self.beatmaps_to_add) > 0:
                self.emit(SIGNAL("copy_widget()"))
                time.sleep(0.02)
            else:
                time.sleep(0.1)

    def copy_widget(self):
        self.add_widget(self.beatmaps_to_add.pop(0))

    def check_for_new_maps(self):
        return len(self.beatmaps_to_add) < 10

    def check_if_add_widget(self):
        return self.items_len < 10

    def pop_exit_dialog(self):
        if ExitDialog.ExitDialog(self).exec_():
            self.close()

    def try_login(self, username, password):
        if type(username) is not str or type(password) is not str:
            logger.error_msg("try_login: Username or password is not string.", None)
            return
        else:
            connector.login(username, password)
        if connector.check_if_logged():
            self.login_action.setEnabled(False)
            self.logout_action.setEnabled(True)
        else:
            self.login_action.setEnabled(True)
            self.logout_action.setEnabled(False)
