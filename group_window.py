from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QGridLayout, QFormLayout,
                             QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QFileSystemModel, QTreeView, QSizePolicy)
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir
import os
import re
import shutil


# The window for creating a note group
class GroupWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowTitle('Create Note Group')
        self.resize(1600, 800)
        self.oldFile = ''

        # Get MainWindow through constructor
        self.mainWindow = mainWindow
        layout = QFormLayout()

        self.fileModel = QFileSystemModel()
        self.fileModel.setOption(QFileSystemModel.DontWatchForChanges, True)
        self.fileModel.setRootPath(
            QDir.currentPath() + '/users/' + self.mainWindow.user)

        self.fileTree = QTreeView()
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(
            self.fileModel.index(QDir.currentPath() + '/users/' + self.mainWindow.user))
        self.fileTree.setColumnWidth(0, 500)
        self.fileTree.doubleClicked.connect(self.doubleClickEvent)
        self.fileTree.clicked.connect(self.selectionChanged)
        layout.addRow(self.fileTree)

        self.fnLineEdit = QLineEdit()
        layout.addRow('Folder Name: ', self.fnLineEdit)

        gridLayout = QGridLayout()
        saveButton = QPushButton('Create')
        saveButton.clicked.connect(self.createEvent)
        saveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        gridLayout.addWidget(saveButton, 0, 0)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)
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
        msg.setWindowTitle('Confirm Group')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.confirmMessageEvent)
        self.confirmResponse = False
        msg.exec_()

    # Displays generic save message to the user
    def createMessageBox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle('Group Info')
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

    # Overrides the QWidget close event
    def closeEvent(self, event):
        self.mainWindow.groupWindow = None

    # Handles double clicking the QTreeView folders/files
    def doubleClickEvent(self):
        if not self.fileModel.isDir(self.fileTree.currentIndex()):
            return
        self.createEvent()

    # Called when the user clicks the 'Create' button
    def createEvent(self):

        fileName, extension = os.path.splitext(
            os.path.basename(self.fnLineEdit.text().strip()))
        subPath = self.fnLineEdit.text().strip().replace(fileName + extension, '')
        filePath = 'users/' + self.mainWindow.user + '/' + subPath + fileName

        # File name cannot be blank
        if self.fnLineEdit.text().strip() == '':
            self.createMessageBox('Please enter a folder name.')
            return

        # Check if file already exists
        if os.path.exists(filePath):
            self.confirmMessageBox(fileName)
            if not self.confirmResponse:
                return

        # Attempt to save file
        if not self.createFolder(filePath):
            self.createMessageBox('Invalid file path.')
            return

        # Close save window
        self.close()

    # Creates a new folder
    def createFolder(self, filePath):
        try:
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
            os.mkdir(filePath)
            return True
        except:
            return False
