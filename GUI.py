import sys
from PyQt4 import QtGui


def main():
    app = QtGui.QApplication([])
    window = QtGui.QWidget()
    window.setGeometry(50, 50, 500, 300)
    window.setWindowTitle("PyQT tuts")
    window.show()
    raw_input()

if __name__ == '__main__':
    main()