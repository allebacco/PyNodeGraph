import sys
sys.path.append('..')

from PyQt4.QtGui import QApplication

from mainwindow import MainWindow


def main():

    app = QApplication([])
    app.setApplicationName("NodeGraphView Example")

    w = MainWindow()
    w.setWindowTitle("NodeGraphView - Example application")

    w.show()
    w.resize(800, 600)

    app.exec_()

    # Workaround for GTK assertion fails on exit
    w = None



if __name__ == '__main__':
    main()