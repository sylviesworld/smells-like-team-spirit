from PyQt5 import QtWidgets, uic, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi("app.ui", self)

    @QtCore.pyqtSlot()
    def newNoteSlot():
        pass

    @QtCore.pyqtSlot()
    def openNoteSlot():
        pass

    @QtCore.pyqtSlot()
    def saveNoteSlot():
        pass

    @QtCore.pyqtSlot()
    def saveAsNoteSlot():
        pass

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('app.ui', self)
        self.show()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    #window = Ui()
    sys.exit(app.exec_())
