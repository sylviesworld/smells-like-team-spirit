from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QGridLayout, QFormLayout,
                             QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QFileSystemModel, QTreeView, QSizePolicy)
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtPrintSupport import QPrinter
from permissions import check_permission, add_permission
from encrypt_file import encrypt_file
import os
import re


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
        layout = QFormLayout()

        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(QDir.currentPath() + '/users/' + self.mainWindow.user)
        filters = ['*.txt']
        self.fileModel.setNameFilters(filters)

        self.fileTree = QTreeView()
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(
            self.fileModel.index(QDir.currentPath() + '/users/' + self.mainWindow.user))
        self.fileTree.setColumnWidth(0, 500)
        self.fileTree.doubleClicked.connect(self.doubleClickEvent)
        self.fileTree.clicked.connect(self.selectionChanged)
        layout.addRow(self.fileTree)

        self.fnLineEdit = QLineEdit()
        layout.addRow('File name: ', self.fnLineEdit)
    
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem('Text Files (*.txt)')
        self.typeComboBox.addItem('PDF Files (*.pdf)')
        layout.addRow('Save as type: ', self.typeComboBox)

        gridLayout = QGridLayout()
        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.saveEvent)
        saveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        gridLayout.addWidget(saveButton, 0, 0)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.closeWindow)
        cancelButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        gridLayout.addWidget(cancelButton, 0, 1)
        layout.addRow(gridLayout)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setLayout(layout)

    # Signal event when the user makes a selection in the QTreeView
    def selectionChanged(self):
        current = self.fileTree.currentIndex()
        removePath = QDir.currentPath() + '/users/' + self.mainWindow.user + '/'
        redata = re.compile(re.escape(removePath), re.IGNORECASE)
        subPath = redata.sub('', self.fileModel.filePath(current))
        
        if os.path.isdir(self.fileModel.filePath(current)):
            subPath += '/'

        self.fnLineEdit.setText(subPath)

    # Displays confirm save message to the user
    def confirmMessageBox(self, fileName):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(fileName + ' already exists.\nDo you want to replace it?')
        msg.setWindowTitle('Confirm Save As')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.confirmMessageEvent)
        self.confirmResponse = False
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

    # Overrides the QWidget show event
    def showEvent(self, event):
        filePath = self.oldFile.replace('users/' + self.mainWindow.user + '/', '')
        self.fnLineEdit.setText(filePath)

    # Overrides the QWidget close event
    def closeEvent(self, event):
        self.mainWindow.saveWindow = None

    # Handles double clicking the QTreeView folders/files
    def doubleClickEvent(self):
        if self.fileModel.isDir(self.fileTree.currentIndex()):
            return
        self.saveEvent()

    # Called when the user clicks the 'Save' button
    def saveEvent(self):

        # Save as new file
        if self.mainWindow.currentFile == '':

            fileName, extension = os.path.splitext(os.path.basename(self.fnLineEdit.text().strip()))
            subPath = self.fnLineEdit.text().strip().replace(fileName + extension, '')
            filePath = 'users/' + self.mainWindow.user + '/' + subPath + fileName

            # File name cannot be blank
            if self.fnLineEdit.text().strip() == '' or fileName.strip() == '':
                self.saveMessageBox('Please enter a file name.')
                return

            # Save text file
            if self.typeComboBox.currentIndex() == 0:
                filePath += '.txt'

                # Check if file already exists
                if os.path.exists(filePath):
                    self.confirmMessageBox(fileName + '.txt')
                    if not self.confirmResponse:
                        return

                # Attempt to save file
                if not self.saveFile(filePath):
                    self.saveMessageBox('Invalid file path.')
                    return

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
                
                # Attempt to save file
                if not self.savePDF(filePath):
                    self.saveMessageBox('Invalid file path.')
                    return

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

        try:
            f = open(filePath, 'wb')
            encrypted = encrypt_file(self.textEdit.toHtml())
            f.write(encrypted)
            f.close()
            return True
        except:
            return False


    # Saves the file as a PDF
    def savePDF(self, filePath):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPrinter.A4)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filePath)
            self.mainWindow.centralWidget.textBox.document().print_(printer)
            return True
        except:
            return False
