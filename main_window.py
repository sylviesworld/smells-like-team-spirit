#!/usr/bin/python3

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

from app_widget import AppWidget

# this class inherits from QMainWindow and will be used to set up the applications GUI
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Get screen resolution
        screenBounds = QDesktopWidget().screenGeometry(0)

        self.setWindowTitle('Notepad App')
        self.setGeometry(0, 0, screenBounds.width() * 0.5, screenBounds.height() * 0.6)

        # Center the screen
        rect = self.frameGeometry()
        centerScreen = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(centerScreen)
        self.move(rect.topLeft())

        # Set central widget for window
        self.centralWidget = AppWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.textBox.textChanged.connect(self.textEditedEvent)

        # Define menu bar
        menuBar = self.menuBar()
        
        # Define file options for menu bar
        fileMenu = menuBar.addMenu('File')

        saveIcon = QIcon.fromTheme('document-save')
        saveButton = QAction(saveIcon, 'Save', self)
        saveButton.setShortcut('Ctrl+S')
        saveButton.triggered.connect(self.saveEvent)
        self.currentFile = ''

        saveAsButton = QAction(saveIcon, 'Save As...', self)
        saveAsButton.setShortcut('Ctrl+Shift+S')
        saveAsButton.triggered.connect(self.saveAsEvent)

        fileMenu.addAction(saveButton)
        fileMenu.addAction(saveAsButton)

    # Called when any key is pressed
    def keyPressEvent(self, e):
        self.statusBar().clearMessage()

    # Called when text in the AppWidget QTextEdit is changed
    def textEditedEvent(self):
        self.statusBar().clearMessage()

    # Opens the file dialog to save a new file, or saves the currently open file
    def saveEvent(self):
        if self.currentFile == '' :
            fileName, _ = QFileDialog.getSaveFileName(self, 'Save As', '', 'Text Files (*.txt)')
            
            if fileName :
                self.centralWidget.saveFile(fileName)
                self.currentFile = fileName
                self.statusBar().showMessage('File saved.')
                return 1

            # File dialog canceled
            return 0

        else :
            self.centralWidget.saveFile(self.currentFile)
            self.statusBar().showMessage('File saved.')
            return 1
    
    # Opens the file dialog even if a file is already open
    def saveAsEvent(self):
        oldFile = self.currentFile
        self.currentFile = ''

        # File dialog canceled, reset to original file name
        if self.saveEvent() == 0 :
            self.currentFile = oldFile
