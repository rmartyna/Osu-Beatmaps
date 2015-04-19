import sys
import os
from PyQt4.QtGui import *
from init import *
import settings
import MyMainWindow


def main():
    settings.load_settings()
    app = QApplication(sys.argv)
    window = MyMainWindow.MyMainWindow()
    window.show()
    app.exec_()
    settings.save_settings()
    ERROR_LOG.close()


if __name__ == "__main__":
    os.chdir("..")
    main()