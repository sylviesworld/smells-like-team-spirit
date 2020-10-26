from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from find_window import FindWindow
from login_window import LoginWindow
from shutil import copyfile
from permissions import check_permission, add_permission
import os
import time
import uuid
import platform

qtcreator_file = "app.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        if 'Darwin' in platform.system():
            icon_size = 18

        else:
            icon_size = 36

        self.setAcceptDrops(True)

        # Get screen resolution
        screenBounds = QDesktopWidget().screenGeometry(0)

        self.window_title = 'Notepad App - untitled.txt'
        self.setWindowTitle(self.window_title)

        self.setGeometry(0, 0, round(screenBounds.width() / 2),
                         round(screenBounds.height() / 2))

        # Center the screen
        rect = self.frameGeometry()
        centerScreen = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(centerScreen)
        self.move(rect.topLeft())

        self.setCentralWidget(self.centralwidget)
        self.textBox_1 = self.findChild(QtWidgets.QTextEdit, 'textEdit')
        self.textBox_1.textChanged.connect(self.textEditedEvent)
        self.textBox_1.cursorPositionChanged.connect(self.cursorMovedEvent)
        self.textBox_1.mainWindow = self
        self.needsSave = False

        #create find window
        self.findWindow = FindWindow(self.textBox_1)

        #new note button
        self.newNoteButton = self.findChild(QtWidgets.QCommandLinkButton, 'commandLinkButton')
        #self.newNoteButton.triggered.connect(lambda: self.openNoteSlot(True))

        #open note button
        self.openNoteButton = self.findChild(QtWidgets.QCommandLinkButton, 'commandLinkButton_2')
        #self.openNoteButton.clicked.connect(lambda: self.openNoteSlot)
            
        #save note button
        self.saveNoteButton = self.findChild(QtWidgets.QCommandLinkButton, 'commandLinkButton_3')
        #self.saveNoteButton.clicked.connect(self.saveNoteSlot)

        #save as button
        self.saveAsButton = self.findChild(QtWidgets.QCommandLinkButton, 'commandLinkButton_4')
        #self.saveAsButton.clicked.connect(self.saveAsNoteSlot)

        # Begin menu bars
        # ===============

        # Define menu bar
        menuBar = self.menuBar
        self.setMenuBar(menuBar)

        # Define status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        #-----------------
        # Create File menu bar
        fileMenu = menuBar.addMenu('File')

        # File menu bar
        newButton = QAction('New', self)
        newButton.setShortcut('Ctrl+N')
        newButton.triggered.connect(lambda: self.newNoteSlot)
        fileMenu.addAction(newButton)

        openButton = QAction('Open...', self)
        openButton.setShortcut('Ctrl+O')
        openButton.triggered.connect(lambda: self.openNoteSlot)
        fileMenu.addAction(openButton)

        closeButton = QAction('Close', self)
        closeButton.setShortcut('Ctrl+W')
        closeButton.triggered.connect(lambda: self.closeEvent)
        fileMenu.addAction(closeButton)

        fileMenu.addSeparator()

        saveIcon = QIcon.fromTheme('document-save')
        saveButton = QAction(saveIcon, 'Save', self)
        saveButton.setShortcut('Ctrl+S')
        saveButton.triggered.connect(self.saveNoteSlot)
        self.currentFile = ''
        fileMenu.addAction(saveButton)

        saveAsButton = QAction(saveIcon, 'Save As...', self)
        saveAsButton.setShortcut('Ctrl+Shift+S')
        saveAsButton.triggered.connect(self.saveAsNoteSlot)
        fileMenu.addAction(saveAsButton)

        printButton = QAction(saveIcon, 'Print', self)
        printButton.setShortcut('Ctrl+P')
        printButton.triggered.connect(self.printEvent)
        fileMenu.addAction(printButton)

        #---------------------
        # Create Edit menu bar
        editMenu = menuBar.addMenu('Edit')

        undoButton = QAction('Undo', self)
        undoButton.setShortcut(QKeySequence.Undo)
        undoButton.triggered.connect(self.textBox_1.undo)
        editMenu.addAction(undoButton)

        redoButton = QAction('Redo', self)
        redoButton.setShortcut(QKeySequence.Redo)
        redoButton.triggered.connect(self.textBox_1.redo)
        editMenu.addAction(redoButton)

        editMenu.addSeparator()

        cutButton = QAction('Cut', self)
        cutButton.setShortcut(QKeySequence.Cut)
        cutButton.triggered.connect(self.textBox_1.cut)
        editMenu.addAction(cutButton)

        copyButton = QAction('Copy', self)
        copyButton.setStatusTip('Copy Selected Text to Clipboard')
        copyButton.setShortcut(QKeySequence.Copy)
        copyButton.triggered.connect(self.textBox_1.copy)
        editMenu.addAction(copyButton)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.setStatusTip('Paste From Clipboard')
        paste_action.triggered.connect(self.textBox_1.paste)
        editMenu.addAction(paste_action)

        editMenu.addSeparator()

        findButton = QAction('Find', self)
        findButton.setShortcut(QKeySequence.Find)
        findButton.triggered.connect(
            self.findWindow.createWindow)
        editMenu.addAction(findButton)

        selectButton = QAction('Select All', self)
        selectButton.setShortcut(QKeySequence.SelectAll)
        selectButton.triggered.connect(self.textBox_1.selectAll)
        editMenu.addAction(selectButton)

        #-----------------------
        # Create Format menu bar
        formatMenu = menuBar.addMenu('Format')

        fontButton = QAction('Fonts...', self)
        fontButton.setShortcut('Ctrl+T')
        fontButton.triggered.connect(self.fontChoice)
        formatMenu.addAction(fontButton)

        self.textBox_1.setTextColor(
            Qt.black)  # Set initial text color HTML
        colorButton = QAction('Font Color...', self)
        colorButton.triggered.connect(self.colorPicker)
        formatMenu.addAction(colorButton)

        imageButton = QAction('Insert Image...', self)
        imageButton.triggered.connect(self.insertImage)
        formatMenu.addAction(imageButton)

        # Begin toolbars
        # ==============

        # --------------------
        # Create edit toolbar
        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(edit_toolbar)

        cut_action = QAction(
            QIcon(os.path.join('images', 'icons8-cut-80.png')), 'Cut', self)
        cut_action.setStatusTip('Cut Selected Text (Copy and Delete)')
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.textBox_1.cut)
        edit_toolbar.addAction(cut_action)

        copy_action = QAction(
            QIcon(os.path.join('images', 'icons8-copy-80.png')), 'Copy', self)
        copy_action.setStatusTip('Copy Selected Text to Clipboard')
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.textBox_1.copy)
        edit_toolbar.addAction(copy_action)

        paste_action = QAction(
            QIcon(os.path.join('images', 'icons8-paste-80.png')), 'Paste', self)
        paste_action.setStatusTip('Paste From Clipboard')
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.textBox_1.paste)
        edit_toolbar.addAction(paste_action)

        imageAction = QAction(
            QIcon(os.path.join('images', 'icons8-add-image-80.png')), 'Image', self)
        imageAction.setStatusTip('Insert an image')
        imageAction.triggered.connect(self.insertImage)
        edit_toolbar.addAction(imageAction)


        # -------------------
        # Create font toolbar
        font_toolbar = QToolBar("Font")
        font_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(font_toolbar)

        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(
            self.textBox_1.setCurrentFont)
        font_toolbar.addWidget(self.fonts)

        FONT_SIZES = [5, 5.5, 6.5, 7.5, 8, 9, 10, 10.5, 11]
        FONT_SIZES.extend(range(12, 30, 2))
        FONT_SIZES.extend([36, 48, 72])

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])
        self.fontsize.currentIndexChanged[str].connect(
            lambda s: self.textBox_1.setFontPointSize(float(s)))
        font_toolbar.addWidget(self.fontsize)

        #----------------------
        # Create format toolbar
        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(format_toolbar)

        self.colorLabel = QLabel()
        self.setColorIcon(Qt.black)
        format_toolbar.addWidget(self.colorLabel)

        colorAction = QAction(
            QIcon(os.path.join('images', 'icons8-text-color-80.png')), 'Font Color', self)
        colorAction.triggered.connect(self.colorPicker)
        format_toolbar.addAction(colorAction)

        bold_action = QAction(
            QIcon(os.path.join('images', 'icons8-bold-80.png')), "Bold", self)
        bold_action.setStatusTip("Set selected text to Bold (strong)")
        bold_action.setShortcut(QKeySequence.Bold)
        bold_action.setCheckable(True)
        bold_action.toggled.connect(lambda x: self.textEdit.setFontWeight(
            QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(bold_action)

        italic_action = QAction(
            QIcon(os.path.join('images', 'icons8-italic-80.png')), "Italic", self)
        italic_action.setStatusTip("Set selected text to Italic (emphasis)")
        italic_action.setShortcut(QKeySequence.Italic)
        italic_action.setCheckable(True)
        italic_action.toggled.connect(self.textEdit.setFontItalic)
        format_toolbar.addAction(italic_action)

        underline_action = QAction(
            QIcon(os.path.join('images', 'icons8-underline-80.png')), "Underline", self)
        underline_action.setStatusTip("Set selected text to Underline")
        underline_action.setShortcut(QKeySequence.Underline)
        underline_action.setCheckable(True)
        underline_action.toggled.connect(
            self.textBox_1.setFontUnderline)
        format_toolbar.addAction(underline_action)

        font = QFont('Helvetica', 16)
        self.textBox_1.setFont(font)
        self.textBox_1.setFontPointSize(16)

        # ------------------------
        # Create paragraph toolbar
        paragraph_toolbar = QToolBar("Paragraph")
        paragraph_toolbar.setIconSize(QSize(icon_size, icon_size))
        self.addToolBar(paragraph_toolbar)

        self.aln_left_action = QAction(
            QIcon(os.path.join('images', 'icons8-align-left-80.png')), "Align Left", self)
        self.aln_left_action.setStatusTip("Align Text Left")
        self.aln_left_action.setCheckable(True)
        self.aln_left_action.triggered.connect(
            lambda: self.textBox_1.setAlignment(Qt.AlignLeft))
        paragraph_toolbar.addAction(self.aln_left_action)

        self.aln_center_action = QAction(
            QIcon(os.path.join('images', 'icons8-align-center-80.png')), "Center", self)
        self.aln_center_action.setStatusTip("Center Text")
        self.aln_center_action.setCheckable(True)
        self.aln_center_action.triggered.connect(
            lambda: self.textBox_1.setAlignment(Qt.AlignCenter))
        paragraph_toolbar.addAction(self.aln_center_action)

        self.aln_right_action = QAction(QIcon(os.path.join(
            'images', 'icons8-align-right-80.png')), "Align Right", self)
        self.aln_right_action.setStatusTip("Align Text Right")
        self.aln_right_action.setCheckable(True)
        self.aln_right_action.triggered.connect(
            lambda: self.textBox_1.setAlignment(Qt.AlignRight))
        paragraph_toolbar.addAction(self.aln_right_action)

        self.aln_justify_action = QAction(
            QIcon(os.path.join('images', 'icons8-align-justify-80.png')), "Justify", self)
        self.aln_justify_action.setStatusTip("Justify Text")
        self.aln_justify_action.setCheckable(True)
        self.aln_justify_action.triggered.connect(
            lambda: self.textBox_1.setAlignment(Qt.AlignJustify))
        paragraph_toolbar.addAction(self.aln_justify_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.aln_left_action)
        format_group.addAction(self.aln_center_action)
        format_group.addAction(self.aln_right_action)
        format_group.addAction(self.aln_justify_action)

    def fontChoice(self):
        font, valid = QFontDialog.getFont()
        if valid:
            # self.styleChoice.setFont(font)
            # self.setFont(font)
            self.textBox_1.setFont(font)

    # Opens the color dialog
    def colorPicker(self):
        cursor = self.textBox_1.textCursor()
        color = QColorDialog.getColor(self.textBox_1.textColor())

        if color.isValid():
            self.setColorIcon(color)
            self.textBox_1.setTextColor(color)

    # Sets the color icon on the QToolBar
    def setColorIcon(self, color):
        pixelMap = QPixmap(64, 24)
        pixelMap.fill(color)
        #self.colorLabel.setPixmap(pixelMap)

    # Called when the QMainWindow is closed
    def closeEvent(self, event):
        if self.needsSave:
            reply = QMessageBox.question(self, 'Window Close',
                                         'Do you want to save changes to the current file?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                self.saveMessageSuccess = self.saveNoteSlot()
                event.accept()

            elif reply == QMessageBox.No:
                event.accept()

            else:
                event.ignore()

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

    # Called when the QTextCursor in the AppWidget QTextEdit is moved
    def cursorMovedEvent(self):

        # Update current text color under cursor for color button display
        self.setColorIcon(self.textBox_1.textColor())

    # Opens the file dialog to save a new file or the working file. Returns false if canceled
    def saveNoteSlot(self):
        if self.currentFile == '':
            fileName, _ = QFileDialog.getSaveFileName(
                self, 'Save As', '', 'Text Files (*.txt);;PDF Files (*.pdf)')

            path, extension = os.path.splitext(fileName)

            # Save text file
            if fileName and extension == '.txt':
                self.saveFile(fileName)
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
            self.saveFile(self.currentFile)
            self.statusBar().showMessage('File saved.')
            self.needsSave = False
            return True

    # Opens the file dialog even if a file is already open. Returns false if canceled
    def saveAsNoteSlot(self):

        oldFile = self.currentFile
        self.currentFile = ''

        # File dialog canceled, reset to original file name
        if self.saveNoteSlot():
            self.currentFile = oldFile
            return False

        return True

    def newNoteSlot(self):
        self.openNoteSlot(True)

     # Opens a file (isNew defines if the file is a new, empty file)
    def openNoteSlot(self, isNew=False):
        print(isNew)

        self.saveMessageSuccess = False

        # Prompt the user to save the working file
        if self.needsSave:
            self.promptSaveMessage()

        # Open file if no save was needed or save was successful
        if not self.needsSave or self.saveMessageSuccess:

            # New file
            if isNew:
                self.textBox_1.clear()
                self.textBox_1.setTextColor(Qt.black)
                self.setColorIcon(Qt.black)
                self.window_title = 'Notepad App - untitled.txt'
                self.setWindowTitle(self.window_title)

            # Open file dialog
            else:
                fileName, _ = QFileDialog.getOpenFileName(
                    self, 'Open File', '', 'Text Files (*.txt *.pdf)')

                can_open = check_permission(
                    self.user, os.path.basename(fileName))
                if fileName and can_open:
                    self.openFile(fileName)
                    self.currentFile = fileName
                    self.window_title = f"'Notepad App - {os.path.basename(fileName)} -- Last Modified - {time.ctime(os.path.getmtime(fileName))}"
                    self.setWindowTitle(self.window_title)

                    # Cursor must be moved to update QTextEdit.textColor member
                    self.textBox_1.moveCursor(
                        QTextCursor.Right, QTextCursor.MoveAnchor)
                    self.setColorIcon(self.textBox_1.textColor())
                    self.textBox_1.moveCursor(
                        QTextCursor.Left, QTextCursor.MoveAnchor)
                elif fileName and not can_open:
                    msg = QMessageBox()
                    if self.user != 'None':
                        msg.setText(
                            self.user + ' does not have permission to open file: ' + os.path.basename(fileName))
                    else:
                        msg.setText(
                            'Sign into account to open private file: ' + os.path.basename(fileName))
                    msg.exec_()

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
            self.saveMessageSuccess = self.saveNoteSlot()

        # Skip saving the file
        elif button.text() == '&No':
            self.needsSave = False

        else:
            return

    # Opens the print dialog
    def printEvent(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialogue = QPrintDialog(printer, self)

        if dialogue.exec_() == QPrintDialog.Accepted:
            self.textBox_1.print_(printer)

    # Saves the file as a PDF
    def savePDF(self, fileName):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(fileName)
        self.textBox_1.document().print_(printer)

    # Opens file and reads the text to QTextEdit
    def openFile(self, fileName):
        f = open(fileName, 'r')
        self.textBox_1.setHtml(f.read())
        f.close()

    # Opens the image file dialog and inserts an image into the QTextEdit
    def insertImage(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, 'Select an Image', '', 'PNG (*.png);;JPEG (*.jpg *.jpeg)')

        if filePath:
            
            # Create image directory
            if not os.path.exists('users/' + self.textBox_1.mainWindow.user + '/images'):
                os.makedirs('users/' + self.textBox_1.mainWindow.user + '/images')

            dest = copyfile(filePath, 'users/' + self.textBox_1.mainWindow.user + '/images/' + os.path.basename(filePath))
            self.textBox_1.textCursor().insertImage(dest)

    # Creaes a new file or opens an existing and saves the QTextEdit text
    def saveFile(self, fileName):
        f = open(fileName, 'w')
        f.write(self.textBox_1.toHtml())
        f.close()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    w = MainWindow()
    login_window.main_window = w

    sys.exit(app.exec_())

'''
    # Opens a file (isNew defines if the file is a new, empty file)
    def openNoteSlot(self):

        self.saveMessageSuccess = False

        # Prompt the user to save the working file
        if self.needsSave:
            self.promptSaveMessage()

        # Open file if no save was needed or save was successful
        if not self.needsSave or self.saveMessageSuccess:

            # Open file dialog
            fileName, _ = QFileDialog.getOpenFileName(
                self, 'Open File', '', 'Text Files (*.txt *.pdf)')

            if fileName:
                f = open(fileName, 'r')
                self.textBox_1.setPlainText(f.read())
                f.close()
                self.openFile(fileName)
                self.currentFile = fileName
                self.setWindowTitle(
                    'Notepad App - ' +
                    os.path.basename(fileName) + ' -- Last Modified - '
                    + time.ctime(os.path.getmtime(fileName)))

            self.needsSave = False

    def newNoteSlot(self):

        self.saveMessageSuccess = False

        # Prompt the user to save the working file
        if self.needsSave:
            self.promptSaveMessage()

        # Open file if no save was needed or save was successful
        if not self.needsSave or self.saveMessageSuccess:
                self.textBox_1.clear()
                self.textBox_1.setTextColor(Qt.black)
                self.setColorIcon(Qt.black)
                self.setWindowTitle('Notepad App - untitled.txt')

        self.needsSave = False
        '''
