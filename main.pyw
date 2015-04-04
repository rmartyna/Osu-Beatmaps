from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


VERSION = "0.1"
DATE = "4th April 2015"
EMAIL = "rmartyna94@gmail.com"
GITHUB = r"https://github.com/rmartyna/Osu-Beatmaps/"

class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        self.set_widget()
        self.loadSettings()
        self.addFileMenu()

        self.setWindowTitle("Osu Beatmaps!")

    def set_widget(self):
        self.main_widget = MyMainWidget()
        self.main_widget.setMinimumSize(800, 450)
        self.setCentralWidget(self.main_widget)

    def loadSettings(self):
        pass

    def addFileMenu(self):
        self.loginAction = self.menuBar().addAction("Login")
        self.connect(self.loginAction, SIGNAL("triggered()"), self.popLoginDialog)

        self.logoutAction = self.menuBar().addAction("Logout")
        self.connect(self.logoutAction, SIGNAL("triggered()"), self.popLogoutDialog)

        self.optionsAction = self.menuBar().addAction("Options")
        self.connect(self.optionsAction, SIGNAL("triggered()"), self.popOptionsDialog)

        self.aboutAction = self.menuBar().addAction("About")
        self.connect(self.aboutAction, SIGNAL("triggered()"), self.popAboutDialog)

    def popLoginDialog(self):
        loginDialog = LoginDialog(self)
        if loginDialog.exec_():
            pass

    def popLogoutDialog(self):
        logoutDialog = LogoutDialog(self)
        if logoutDialog.exec_():
            pass

    def popOptionsDialog(self):
        optionsDialog = OptionsDialog(self)
        if optionsDialog.exec_():
            pass

    def popAboutDialog(self):
        aboutDialog = AboutDialog(self)
        if aboutDialog.exec_():
            pass



class MyMainWidget(QWidget):

    def __init__(self, parent=None):
        super(MyMainWidget, self).__init__(parent)

        self.addButtons()

    def addButtons(self):
        self.layout = QVBoxLayout(self)

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.label1 = QLabel()
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)


class LoginDialog(QDialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        usernameLabel = QLabel("Username: ", self)
        self.username = QLineEdit(self)
        passwordLabel = QLabel("Password: ", self)
        self.password = QLineEdit(self)
        self.usernameCheckBox = QCheckBox("Remember username ", self)
        self.passwordCheckBox = QCheckBox("Remember password ", self)
        self.okButton = QPushButton("OK", self)
        self.cancelButton = QPushButton("Cancel", self)

        layout = QGridLayout()
        layout.addWidget(usernameLabel, 0, 0)
        layout.addWidget(self.username, 0, 1)
        layout.addWidget(passwordLabel, 1, 0)
        layout.addWidget(self.password, 1, 1)
        layout.addWidget(self.usernameCheckBox, 2, 0, 1, 2)
        layout.addWidget(self.passwordCheckBox, 3, 0, 1, 2)
        layout.addWidget(self.okButton, 4, 0)
        layout.addWidget(self.cancelButton, 4, 1)
        self.setLayout(layout)

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
         {3}</p>""".format(VERSION, DATE,
                                   EMAIL, GITHUB), self)
        self.button = QPushButton("OK", self)
        self.button.setMaximumWidth(100)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.button, 0, Qt.AlignCenter)
        self.setLayout(layout)

        self.setWindowTitle("About")

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()