import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import settings
import MyMainWindow


def main():
    settings.load_settings()
    app = QApplication(sys.argv)
    window = MyMainWindow.MyMainWindow()
    window.show()
    app.exec_()
    settings.save_settings()

if __name__ == "__main__":
    main()