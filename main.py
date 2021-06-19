from PyQt5 import QtWidgets, QtCore, QtGui
from myLibrary.MainWindow import MainWindow

import traceback
import sys


def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)


def start():
    import sys
    sys.excepthook = show_exception_and_exit
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    w = MainWindow()
    w.show()  # Показываем окно
    app.exec_()  # Запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    start()  # то запускаем функцию main()
