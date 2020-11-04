from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QFileSystemModel, QTreeView)
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtPrintSupport import QPrinter
from permissions import check_permission, add_permission
from encrypt_file import encrypt_file
import os


# The window for saving a file
class SaveWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowTitle('Save As')
        self.resize(1600, 800)
        self.oldFile = ''

        # Get MainWindow through constructor
        self.mainWindow = mainWindow
        self.closeOnSave = False
        self.textEdit = mainWindow.centralWidget.textBox
        layout = QGridLayout()

        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(QDir.currentPath() + '/users/')

        self.fileTree = QTreeView()
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(
            self.fileModel.index(QDir.currentPath() + '/users/'))
        self.fileTree.setColumnWidth(0, 500)
        self.fileTree.doubleClicked.connect(self.saveEvent)

        layout.addWidget(self.fileTree, 0, 0)

        fnLabel = QLabel('File name: ')
        self.fnLineEdit = QLineEdit()
        layout.addWidget(fnLabel, 1, 0)
        layout.addWidget(self.fnLineEdit, 1, 1)

        typeLabel = QLabel('Save as type: ')
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem('Text Files (*.txt)')
        self.typeComboBox.addItem('PDF Files (*.pdf)')
        layout.addWidget(typeLabel, 2, 0)
        layout.addWidget(self.typeComboBox, 2, 1)

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.saveEvent)
        layout.addWidget(saveButton, 3, 0)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.closeWindow)
        layout.addWidget(cancelButton, 3, 1)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setLayout(layout)

    # Displays confirm save message to the user
    def confirmMessageBox(self, fileName):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(fileName + ' already exists.\nDo you want to replace it?')
        msg.setWindowTitle('Confirm Save As')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.confirmMessageEvent)
        msg.exec_()

    # Displays generic save message to the user
    def saveMessageBox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle('Save Info')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # Handles the response to the confirm message box
    def confirmMessageEvent(self, button):

        if button.text() == '&Yes':
            self.confirmResponse = True

        # Skip saving the file
        elif button.text() == '&No':
            self.confirmResponse = False

        else:
            self.confirmResponse = False

    # Closes the save window
    def closeWindow(self):

        # Restore old file from Save As event if window closed
        if self.oldFile != '':
            self.mainWindow.currentFile = self.oldFile
            self.oldFile = ''

        self.close()

    def closeEvent(self, event):
        self.mainWindow.saveWindow = None

    # Called when the user clicks the 'Save' button
    def saveEvent(self):

        # Save as new file
        if self.mainWindow.currentFile == '':

            # File name cannot be blank
            if self.fnLineEdit.text().strip() == '':

                self.saveMessageBox('Please enter a file name.')
                return

            fileName, extension = os.path.splitext(
                self.fnLineEdit.text().strip())
            filePath = 'users/' + self.mainWindow.user + '/' + fileName

            # Save text file
            if self.typeComboBox.currentIndex() == 0:
                filePath += '.txt'

                # Check if file already exists
                if os.path.exists(filePath):
                    self.confirmMessageBox(fileName + '.txt')
                    if not self.confirmResponse:
                        return

                self.saveFile(filePath)
                self.mainWindow.currentFile = filePath
                self.mainWindow.statusBar().showMessage('File saved.')
                self.mainWindow.needsSave = False
                self.mainWindow.window_title = f'Notepad App - {os.path.basename(filePath)}'
                self.mainWindow.setWindowTitle(self.mainWindow.window_title)
                add_permission(self.mainWindow.user, filePath)

            # Save PDF
            else:
                filePath += '.pdf'

                # Check if file already exists
                if os.path.exists(filePath):
                    self.confirmMessageBox(fileName + '.pdf')
                    if not self.confirmResponse:
                        return

                # Run through Save As button; reset
                if self.oldFile != '':
                    self.mainWindow.currentFile = self.oldFile
                    self.oldFile = ''

                self.savePDF(filePath)
                add_permission(self.mainWindow.user, filePath)

            # Close save window
            self.close()

        # Save working file
        else:
            self.saveFile(self.mainWindow.currentFile)
            self.mainWindow.statusBar().showMessage('File saved.')
            self.mainWindow.needsSave = False
            self.mainWindow.window_title = f'Notepad App - {os.path.basename(self.mainWindow.currentFile)}'
            self.mainWindow.setWindowTitle(self.mainWindow.window_title)
            add_permission(self.mainWindow.user, self.mainWindow.currentFile)

        # Close the application after save if needed
        if self.closeOnSave:
            QtCore.QCoreApplication.exit(0)

    # Called when the user clicks the 'Save As' button
    def saveAsEvent(self):
        self.oldFile = self.mainWindow.currentFile
        self.mainWindow.currentFile = ''
        self.show()

    # Decides whether to open the save window or not when the user saves
    def initSaveEvent(self):
        if self.mainWindow.currentFile == '':
            self.show()
        else:
            self.saveEvent()
            self.close()

    # Creates a new file or opens an existing one and saves the QTextEdit text
    def saveFile(self, filePath):
        f = open(filePath, 'wb')
        encrypted = encrypt_file(self.textEdit.toHtml())
        f.write(encrypted)
        f.close()

    # Saves the file as a PDF
    def savePDF(self, filePath):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filePath)
        self.mainWindow.centralWidget.textBox.document().print_(printer)
