import os
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from app_widget import AppWidget

# this class inherits from QMainWindow and will be used to set up the applications GUI
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Get screen resolution
        screenBounds = QDesktopWidget().screenGeometry(0)

        self.window_title = 'Notepad App - untitled.txt'
        self.setWindowTitle(self.window_title)

        self.setGeometry(0, 0, screenBounds.width() *
                         0.5, screenBounds.height() * 0.6)

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

        font = QFont('Helvetica', 20)
        self.centralWidget.textBox.setFont(font)
        self.centralWidget.textBox.setFontPointSize(20)

        # Define menu bar
        menuBar = self.menuBar()

        # Define status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Create menu bars
        fileMenu = menuBar.addMenu('File')

        formatMenu = menuBar.addMenu('Format')

        # File menu bar
        newButton = QAction('New', self)
        newButton.setShortcut('Ctrl+N')
        newButton.triggered.connect(lambda: self.openEvent(True))
        fileMenu.addAction(newButton)

        openButton = QAction('Open...', self)
        openButton.setShortcut('Ctrl+O')
        openButton.triggered.connect(lambda: self.openEvent(False))
        fileMenu.addAction(openButton)

        closeButton = QAction('Close', self)
        closeButton.setShortcut('Ctrl+W')
        closeButton.triggered.connect(lambda: self.closeEvent)
        fileMenu.addAction(closeButton)

        fileMenu.addSeparator()

        saveIcon = QIcon.fromTheme('document-save')
        saveButton = QAction(saveIcon, 'Save', self)
        saveButton.setShortcut('Ctrl+S')
        saveButton.triggered.connect(self.saveEvent)
        self.currentFile = ''
        fileMenu.addAction(saveButton)

        saveAsButton = QAction(saveIcon, 'Save As...', self)
        saveAsButton.setShortcut('Ctrl+Shift+S')
        saveAsButton.triggered.connect(self.saveAsEvent)
        fileMenu.addAction(saveAsButton)

        printButton = QAction(saveIcon, 'Print', self)
        printButton.setShortcut('Ctrl+P')
        printButton.triggered.connect(self.printEvent)
        fileMenu.addAction(printButton)

        # Edit menu bar
        editMenu = menuBar.addMenu('Edit')

        undoButton = QAction('Undo', self)
        undoButton.setShortcut(QKeySequence.Undo)
        undoButton.triggered.connect(self.centralWidget.textBox.undo)
        editMenu.addAction(undoButton)

        redoButton = QAction('Redo', self)
        redoButton.setShortcut(QKeySequence.Redo)
        redoButton.triggered.connect(self.centralWidget.textBox.redo)
        editMenu.addAction(redoButton)

        editMenu.addSeparator()

        cutButton = QAction('Cut', self)
        cutButton.setShortcut(QKeySequence.Cut)
        cutButton.triggered.connect(self.centralWidget.textBox.cut)
        editMenu.addAction(cutButton)

        copyButton = QAction('Copy', self)
        copyButton.setStatusTip('Copy Selected Text to Clipboard')
        copyButton.setShortcut(QKeySequence.Copy)
        copyButton.triggered.connect(self.centralWidget.textBox.copy)
        editMenu.addAction(copyButton)

        # Duplicate paste edit menu button
        # pasteButton = QAction('Paste', self)
        # pasteButton.setShortcut(QKeySequence.Paste)
        # pasteButton.triggered.connect(self.centralWidget.textBox.paste)
        # editMenu.addAction(pasteButton)

        # Format menu button
        # fontButton = QAction('Font', self)
        # fontButton.triggered.connect(self.fontChoice)
        # formatMenu.addAction(fontButton)

        # Create toolbars
        # file_toolbar = QToolBar("File")
        # file_toolbar.setIconSize(QSize(18, 18))
        # self.addToolBar(file_toolbar)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.setStatusTip('Paste From Clipboard')
        paste_action.triggered.connect(self.centralWidget.textBox.paste)
        editMenu.addAction(paste_action)

        selectButton = QAction('Select All', self)
        selectButton.setShortcut(QKeySequence.SelectAll)
        selectButton.triggered.connect(self.centralWidget.textBox.selectAll)
        editMenu.addAction(selectButton)

        findButton = QAction('Find', self)
        findButton.setShortcut(QKeySequence.Find)
        findButton.triggered.connect(self.centralWidget.findWindow.createWindow)
        editMenu.addAction(findButton)

        # File toolbar
        # open_file_action = QAction("Open...", self)
        # open_file_action.setStatusTip("Open an Existing File")
        # open_file_action.triggered.connect(self.openEvent)
        # file_toolbar.addAction(open_file_action)

        # Format menu button
        fontButton = QAction('Font System Dialogue', self)
        fontButton.triggered.connect(self.fontChoice)
        formatMenu.addAction(fontButton)

        # save_file_action = QAction(saveIcon, 'Save', self)
        # save_file_action.setStatusTip('Save Changes to Current File')
        # save_file_action.triggered.connect(self.saveEvent)
        # self.currentFile = ''
        # file_toolbar.addAction(save_file_action)

        # save_as_action = QAction(saveIcon, 'Save As...', self)
        # save_as_action.setStatusTip("Save Current Note to Specified File")
        # save_as_action.triggered.connect(self.saveAsEvent)
        # file_toolbar.addAction(save_as_action)

        # Create edit toolbar
        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(edit_toolbar)

        copy_action = QAction('Copy', self)
        copy_action.setStatusTip('Copy Selected Text to Clipboard')
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.centralWidget.textBox.copy)
        edit_toolbar.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setStatusTip('Paste From Clipboard')
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.centralWidget.textBox.paste)
        edit_toolbar.addAction(paste_action)

        font_choice_action = QAction('Font', self)
        font_choice_action.setStatusTip(
            'Open System Dialogue for Font Choice')
        font_choice_action.triggered.connect(self.fontChoice)
        edit_toolbar.addAction(font_choice_action)

        # Create format toolbar
        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(format_toolbar)

        bold_action = QAction("Bold", self)
        bold_action.setStatusTip("Set font to Bold (strong)")
        bold_action.setShortcut(QKeySequence.Bold)
        bold_action.setCheckable(True)
        bold_action.toggled.connect(lambda x: self.centralWidget.textBox.setFontWeight(
            QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(bold_action)
        formatMenu.addAction(bold_action)

        italic_action = QAction("Italic", self)
        italic_action.setStatusTip("Set font to Italic (emphasis)")
        italic_action.setShortcut(QKeySequence.Italic)
        italic_action.setCheckable(True)
        italic_action.toggled.connect(self.centralWidget.textBox.setFontItalic)
        format_toolbar.addAction(italic_action)
        formatMenu.addAction(italic_action)

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
        if "Edited" not in str(self.window_title):
            self.window_title = self.window_title + " -- Edited"
            self.setWindowTitle(self.window_title)

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
                self.window_title = f'Notepad App - {os.path.basename(fileName)}'
                self.setWindowTitle(self.window_title)
                return True

            # Save PDF
            elif fileName and extension == '.pdf':
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
                self.window_title = 'Notepad App - untitled.txt'
                self.setWindowTitle(self.window_title)

            # Open file dialog
            else:
                fileName, _ = QFileDialog.getOpenFileName(
                    self, 'Open File', '', 'Text Files (*.txt *.pdf)')

                if fileName:
                    self.centralWidget.openFile(fileName)
                    self.currentFile = fileName
                    self.window_title = f"'Notepad App - {os.path.basename(fileName)} -- Last Modified - {time.ctime(os.path.getmtime(fileName))}"
                    self.setWindowTitle(self.window_title)

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
    def printEvent(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialogue = QPrintDialog(printer, self)

        if dialogue.exec_() == QPrintDialog.Accepted:
            self.centralWidget.textBox.print_(printer)

    # Saves the file as a PDF
    def savePDF(self, fileName):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(fileName)
        self.centralWidget.textBox.document().print_(printer)
