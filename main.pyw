from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        pass


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()