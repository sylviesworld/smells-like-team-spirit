#!/usr/bin/python3

import os
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFontDialog, QColorDialog, QTextEdit
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from app_widget import AppWidget

# this class inherits from QMainWindow and will be used to set up the applications GUI
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Get screen resolution
        screenBounds = QDesktopWidget().screenGeometry(0)

        self.setWindowTitle('Notepad App - untitled.txt')
        self.setGeometry(0, 0, screenBounds.width() *
                         0.5, screenBounds.height() * 0.6)

        # self.setWindowIcon(QtGui.QIcon(
        #   'paper-calendar-notepad-notebook-png-favpng-cZMwKJMjDvrcDcGFdxhcgHAbd_t.jpg'))

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

        # Define menu bar
        menuBar = self.menuBar()

        # Define file options for menu bar
        fileMenu = menuBar.addMenu('File')

        newButton = QAction('New', self)
        newButton.setShortcut('Ctrl+N')
        newButton.triggered.connect(lambda: self.openEvent(True))

        openButton = QAction('Open...', self)
        openButton.setShortcut('Ctrl+O')
        openButton.triggered.connect(lambda: self.openEvent(False))

        saveIcon = QIcon.fromTheme('document-save')
        saveButton = QAction(saveIcon, 'Save', self)
        saveButton.setShortcut('Ctrl+S')
        saveButton.triggered.connect(self.saveEvent)
        self.currentFile = ''

        saveAsButton = QAction(saveIcon, 'Save As...', self)
        saveAsButton.setShortcut('Ctrl+Shift+S')
        saveAsButton.triggered.connect(self.saveAsEvent)

        fileMenu.addAction(newButton)
        fileMenu.addAction(openButton)
        fileMenu.addAction(saveButton)
        fileMenu.addAction(saveAsButton)

        editMenu = menuBar.addMenu('Edit')

        editButton = QAction('yo dude', self)
        editMenu.addAction(editButton)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)

        # open_file_action = QAction(QIcon(os.path.join(
        #     'images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action = QAction("Open File", self)
        open_file_action.setStatusTip("Open a file")
        open_file_action.triggered.connect(self.openEvent)
        file_toolbar.addAction(open_file_action)

        font_choice = QAction('Font', self)
        font_choice.triggered.connect(self.fontChoice)
        # file_toolbar.addToolBar(font_choice)
        file_toolbar.addAction(font_choice)
        # self.file_toolbar.addAction(font_choice)

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
                self, 'Save As', '', 'Text Files (*.txt)')

            if fileName:
                self.centralWidget.saveFile(fileName)
                self.currentFile = fileName
                self.statusBar().showMessage('File saved.')
                self.needsSave = False
                self.setWindowTitle('Notepad App - ' +
                                    os.path.basename(fileName))
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
    def openEvent(self, isNew: bool):

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
                    self, 'Open File', '', 'Text Files (*.txt)')

                if fileName:
                    self.centralWidget.openFile(fileName)
                    self.currentFile = fileName
                    self.setWindowTitle(
                        'Notepad App - ' + os.path.basename(fileName))

            self.needsSave = False

    # Creates the save message prompt window
    def promptSaveMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Do you want to save changes to the current file?')
        msg.setWindowTitle('Notepad App Message')
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
