from PySide2.QtWidgets import QApplication
from mainwin import MyMainWin


def main():
    app = QApplication()
    w = MyMainWin()
    w.show()
    app.exec_()


if __name__ == '__main__':
    main()
