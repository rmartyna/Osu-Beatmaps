import sys
from PyQt4.QtGui import *
import settings
import MyMainWindow
import init
import os


def main():
    settings.load_settings()
    app = QApplication(sys.argv)
    window = MyMainWindow.MyMainWindow()
    window.show()
    app.exec_()
    settings.save_settings()
    init.ERROR_LOG.close()


if __name__ == "__main__":
    os.chdir("..")
    main()