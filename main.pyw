import sys
import pickle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from init import *


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        self.load_settings()
        self.connect_to_osu()
        if PASSWORD is not None:
            self.try_login(USERNAME, PASSWORD)
        self.set_widget()
        self.add_file_menu()

        self.setWindowTitle("Osu Beatmaps!")

    def set_widget(self):
        self.main_widget = MyMainWidget()
        self.main_widget.setMinimumSize(800, 450)
        self.setCentralWidget(self.main_widget)

    def load_settings(self):
        global USERNAME, PASSWORD, DOWNLOAD_FOLDER
        try:
            settings = pickle.load(open("config.dat", "rb"))
        except IOError:
            settings = dict()

        try:
            USERNAME = settings["username"]
        except KeyError:
            pass
        try:
            PASSWORD = settings["password"]
        except KeyError:
            pass
        try:
            DOWNLOAD_FOLDER = settings["download_folder"]
        except KeyError:
            pass

    def connect_to_osu(self):


    def add_file_menu(self):
        self.login_action = self.menuBar().addAction("Login")
        self.connect(self.login_action, SIGNAL("triggered()"), self.pop_login_dialog)

        self.logout_action = self.menuBar().addAction("Logout")
        self.connect(self.logout_action, SIGNAL("triggered()"), self.pop_logout_dialog)
        if PASSWORD is None:
            self.logout_action.setCheckable(False)
        else:
            self.login_action.setCheckable(True)

        self.options_action = self.menuBar().addAction("Options")
        self.connect(self.options_action, SIGNAL("triggered()"), self.pop_options_dialog)

        self.about_action = self.menuBar().addAction("About")
        self.connect(self.about_action, SIGNAL("triggered()"), self.pop_about_dialog)

    def pop_login_dialog(self):
        login_dialog = LoginDialog(self)
        if login_dialog.exec_():
            print("accepted")

    def pop_logout_dialog(self):
        global PASSWORD
        logout_dialog = LogoutDialog(self)
        if logout_dialog.exec_():
            PASSWORD = None
            self.logout_action.setCheckable(False)
            self.login_action.setCheckable(True)

    def pop_options_dialog(self):
        options_dialog = OptionsDialog(self)
        if options_dialog.exec_():
            print("accepted")

    def pop_about_dialog(self):
        AboutDialog(self).exec_()

    def try_login(self, username, password):
        pass



class MyMainWidget(QWidget):

    def __init__(self, parent=None):
        super(MyMainWidget, self).__init__(parent)

        self.add_buttons()

    def add_buttons(self):
        self.layout = QVBoxLayout(self)

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.label1 = QLabel()
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)


class LoginDialog(QDialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        username_label = QLabel("Username: ", self)
        if USERNAME is None:
            self.username = QLineEdit(self)
        else:
            self.username = QLineEdit(USERNAME, self)
        password_label = QLabel("Password: ", self)
        self.password = QLineEdit(self)
        self.username_check_box = QCheckBox("Remember username ", self)
        if USERNAME is not None:
            self.username_check_box.setChecked()
        self.password_check_box = QCheckBox("Remember password ", self)
        self.login_button = QPushButton("Login", self)
        self.cancel_button = QPushButton("Cancel", self)

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

        self.connect(self.okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.cancelButton, SIGNAL("clicked()"), self, SLOT("reject()"))

        self.setWindowTitle("Login")


class LogoutDialog(QDialog):

    def __init__(self, parent=None):
        super(LogoutDialog, self).__init__(parent)

        label = QLabel("Are you sure you want to logout?", parent)
        self.yesButton = QPushButton("Yes", parent)
        self.noButton = QPushButton("No", parent)

        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.yesButton, 1, 0)
        layout.addWidget(self.noButton, 1, 1)
        self.setLayout(layout)

        self.connect(self.yesButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.noButton, SIGNAL("clicked()"), self, SLOT("reject()"))

        self.windowTitle("Logout")



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
         {3}</p>""".format(init.VERSION, DATE,
                                   EMAIL, GITHUB), self)
        self.button = QPushButton("OK", self)
        self.button.setMaximumWidth(100)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.button, 0, Qt.AlignCenter)
        self.setLayout(layout)

        self.connect(self.button, SIGNAL("clicked()"), self, SLOT("accept()"))

        self.setWindowTitle("About")

def main():
    init.init()
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()