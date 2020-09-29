from PyQt5 import QtWidgets, uic, QtCore
import os
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from app_widget import AppWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi("app.ui", self)

         # Get screen resolution
        screenBounds = QDesktopWidget().screenGeometry(0)

        self.setWindowTitle('Notepad App - untitled.txt')
        self.setGeometry(0, 0, round(screenBounds.width()/2), round(screenBounds.height()/2))

        # Center the screen
        rect = self.frameGeometry()
        centerScreen = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(centerScreen)
        self.move(rect.topLeft())

        # Set central widget for window
        self.centralWidget = AppWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.textBox.textChanged.connect(self.textEditedEvent)
        self.needsSave = False

    def fontChoice(self):
        font, valid = QFontDialog.getFont()
        if valid:
            # self.styleChoice.setFont(font)
            self.setFont(font)

    # Called when the QMainWindow is closed
    def closeEvent(self, event):
        if self.needsSave:
            self.promptSaveMessage()

    # Called when any key is pressed
    def keyPressEvent(self, e):
        self.statusBar().clearMessage()

    # Called when text in the AppWidget QTextEdit is changed
    def textEditedEvent(self):
        self.needsSave = True
        self.statusBar().clearMessage()


          # Opens the file dialog to save a new file or the working file. Returns false if canceled
    def saveEvent(self):
        if self.currentFile == '':
            fileName, _ = QFileDialog.getSaveFileName(
                self, 'Save As', '', 'Text Files (*.txt);;PDF Files (*.pdf)')

            path, extension = os.path.splitext(fileName)

            # Save text file
            if fileName and extension == '.txt':
                self.centralWidget.saveFile(fileName)
                self.currentFile = fileName
                self.statusBar().showMessage('File saved.')
                self.needsSave = False
                self.setWindowTitle('Notepad App - ' +
                                    os.path.basename(fileName))
                return True
            
            # Save PDF
            elif fileName and extension == '.pdf' :
                self.savePDF(fileName)
                return True

            # File dialog canceled
            return False

        else:
            self.centralWidget.saveFile(self.currentFile)
            self.statusBar().showMessage('File saved.')
            self.needsSave = False
            return True

    # Opens the file dialog even if a file is already open. Returns false if canceled
    def saveAsEvent(self):

        oldFile = self.currentFile
        self.currentFile = ''

        # File dialog canceled, reset to original file name
        if self.saveEvent():
            self.currentFile = oldFile
            return False

        return True

    # Opens a file (isNew defines if the file is a new, empty file)
    def openNoteSlot(self, isNew: bool):

        self.saveMessageSuccess = False

        # Prompt the user to save the working file
        if self.needsSave:
            self.promptSaveMessage()

        # Open file if no save was needed or save was successful
        if not self.needsSave or self.saveMessageSuccess:

            # New file
            if isNew:
                self.centralWidget.textBox.clear()
                self.setWindowTitle('Notepad App - untitled.txt')

            # Open file dialog
            else:
                fileName, _ = QFileDialog.getOpenFileName(
                    self, 'Open File', '', 'Text Files (*.txt *.pdf)')

                if fileName:
                    self.centralWidget.openFile(fileName)
                    self.currentFile = fileName
                    self.setWindowTitle(
                        'Notepad App - ' + os.path.basename(fileName) + ' -- Last Modified - ' + time.ctime(os.path.getmtime(fileName)))

            self.needsSave = False

    # Creates the save message prompt window
    def promptSaveMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Do you want to save changes to the current file?')
        msg.setWindowTitle('Notepad App Save Message')
        msg.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.saveMessageEvent)
        msg.exec_()

    # Handles the save prompt button event when opening a new file
    def saveMessageEvent(self, button):

        # Save the file and store the result
        if button.text() == '&Yes':
            self.saveMessageSuccess = self.saveEvent()

        # Skip saving the file
        elif button.text() == '&No':
            self.needsSave = False

    # Opens the print dialog
    def printEvent(self) :
        printer = QPrinter(QPrinter.HighResolution)
        dialogue = QPrintDialog(printer, self)
        
        if dialogue.exec_() == QPrintDialog.Accepted :
            self.centralWidget.textBox.print_(printer)

    # Saves the file as a PDF
    def savePDF(self, fileName) :
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(fileName)
        self.centralWidget.textBox.document().print_(printer)


    @QtCore.pyqtSlot()
    def newNoteSlot():
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
    sys.exit(app.exec_())
