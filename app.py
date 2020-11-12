"""Implements note taking interface for app.py
Reference main_window, the same code that drives main.py,
for documentation on each method."""

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from find_window import FindWindow
from account_windows import LoginWindow
from shutil import copyfile
from permissions import check_permission, add_permission
import os
import time
import uuid
import platform
from AppOpenWindow import AppOpenWindow
from AppSaveWindow import AppSaveWindow
from find_window import FindWindow

qtcreator_file = "app.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

FONT_SIZES = [5, 5.5, 6.5, 7.5, 8, 9, 10, 10.5, 11]
FONT_SIZES.extend(range(12, 30, 2))
FONT_SIZES.extend([36, 48, 72])


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        if 'Darwin' in platform.system():
            icon_size = 18

        else:
            icon_size = 36

        self.Edited = False

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

        # Create save window and open window
        self.saveWindow = None
        self.openWindow = None
        self.saveMessageCancel = False

        # create find window
        self.findWindow = FindWindow(self.textBox_1)

        # new note button
        self.newNoteButton = self.findChild(
            QtWidgets.QCommandLinkButton, 'commandLinkButton')

        # open note button
        self.openNoteButton = self.findChild(
            QtWidgets.QCommandLinkButton, 'commandLinkButton_2')

        # save note button
        self.saveNoteButton = self.findChild(
            QtWidgets.QCommandLinkButton, 'commandLinkButton_3')

        # save as button
        self.saveAsButton = self.findChild(
            QtWidgets.QCommandLinkButton, 'commandLinkButton_4')

        # Begin menu bars
        # ===============

        # Define menu bar
        menuBar = self.menuBar
        self.setMenuBar(menuBar)

        # Define status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # -----------------
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

        # ---------------------
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

        # -----------------------
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

        findAction = QAction(
            QIcon(os.path.join('images', 'icons8-search-80.png')), 'Find', self)
        findAction.setStatusTip('Open Find Text Window')
        findAction.setShortcut(QKeySequence.Find)
        findWindow = FindWindow(self.textBox_1)
        findAction.triggered.connect(
            findWindow.createWindow)
        edit_toolbar.addAction(findAction)

        # -------------------
        # Create font toolbar
        font_toolbar = QToolBar("Font")
        font_toolbar.setIconSize(QSize(icon_size, icon_size))
        self.addToolBar(font_toolbar)

        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(
            self.textBox_1.setCurrentFont)
        font_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])
        self.fontsize.setCurrentIndex(FONT_SIZES.index(16))
        self.fontsize.currentIndexChanged[str].connect(
            lambda s: self.textBox_1.setFontPointSize(float(s)))
        font_toolbar.addWidget(self.fontsize)

        FONT_COLORS = ["Black", "Red", "Green",
                       "Blue", "Yellow", "Gray", "Magenta"]

        self.fontcolor = QComboBox()
        self.fontcolor.addItems(FONT_COLORS)
        self.fontcolor.setCurrentIndex(FONT_COLORS.index("Black"))
        self.fontcolor.currentIndexChanged.connect(self.TextColor)
        font_toolbar.addWidget(self.fontcolor)

        # ---------------------
        # Create format toolbar
        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(icon_size, icon_size))
        self.addToolBar(format_toolbar)

        self.colorLabel = QLabel()
        self.setColorIcon(Qt.black)
        format_toolbar.addWidget(self.colorLabel)

        colorAction = QAction(
            QIcon(os.path.join('images', 'icons8-text-color-80.png')), 'Font Color', self)
        colorAction.setStatusTip('Select Font Color')
        colorAction.triggered.connect(self.colorPicker)
        format_toolbar.addAction(colorAction)

        self.highlightLabel = QLabel()
        self.setHighlightIcon(Qt.white)
        self.textBox_1.setTextBackgroundColor(Qt.white)
        format_toolbar.addWidget(self.highlightLabel)

        highlightAction = QAction(
            QIcon(os.path.join('images', 'icons8-marker-pen-80.png')), 'Text Highlight Color', self)
        highlightAction.setStatusTip('Select Text Highlighting Color')
        highlightAction.triggered.connect(self.highlightPicker)
        format_toolbar.addAction(highlightAction)

        self.bold_action = QAction(
            QIcon(os.path.join('images', 'icons8-bold-80.png')), "Bold", self)
        self.bold_action.setStatusTip("Set selected text to Bold (strong)")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.textBox_1.setFontWeight(
            QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)

        self.italic_action = QAction(
            QIcon(os.path.join('images', 'icons8-italic-80.png')), "Italic", self)
        self.italic_action.setStatusTip(
            "Set selected text to Italic (emphasis)")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(
            self.textBox_1.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        # formatMenu.addAction(italic_action)

        self.underline_action = QAction(
            QIcon(os.path.join('images', 'icons8-underline-80.png')), "Underline", self)
        self.underline_action.setStatusTip("Set selected text to Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(
            self.textBox_1.setFontUnderline)
        format_toolbar.addAction(self.underline_action)

        bullet_action = QAction(
            QIcon(os.path.join('images', 'icons8-bulleted-list-80.png')), "Bulleted List", self)
        bullet_action.setStatusTip('Add a Bullet List')
        bullet_action.triggered.connect(self.BulletList)
        format_toolbar.addAction(bullet_action)

        numbered_action = QAction(
            QIcon(os.path.join('images', 'icons8-numbered-list-80.png')), "Numbered List", self)
        numbered_action.setStatusTip('Add a Numbered List')
        numbered_action.triggered.connect(self.NumberedList)
        format_toolbar.addAction(numbered_action)

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

        self.aln_left_action.setChecked(True)
        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.aln_left_action)
        format_group.addAction(self.aln_center_action)
        format_group.addAction(self.aln_right_action)
        format_group.addAction(self.aln_justify_action)

    def BulletList(self):
        textSelected = self.textBox_1.textCursor().selectedText()

        if textSelected == '':
            self.textBox_1.insertHtml("<ul><li>_</li></ul>")

        else:
            self.textBox_1.insertHtml(
                "<ul><li>" + textSelected + "</li></ul>")

    def NumberedList(self):
        textSelected = self.textBox_1.textCursor().selectedText()

        if textSelected == '':
            self.textBox_1.insertHtml("<ol><li>_</li></ol>")

        else:
            self.textBox_1.insertHtml(
                "<ol><li>" + textSelected + "</li></ol>")

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

    # Opens the highlight color dialog
    def highlightPicker(self):
        color = QColorDialog.getColor(
            self.textBox_1.textBackgroundColor())

        if color.isValid():
            self.setHighlightIcon(color)
            self.textBox_1.setTextBackgroundColor(color)

    def SearchSelection(self):
        cursor = self.textBox_1.textCursor()
        textSelected = cursor.selectedText()
        flags = QTextDocument.FindFlags()
        r = self.textBox_1.find(textSelected, flags)

        if not r:
            self.textBox_1.moveCursor(QTextCursor.Start)
            r = self.textBox_1.find(textSelected, flags)

            if not r:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText('Text Not Found.')
                msg.setWindowTitle('Error')
                msg.exec_()

        return r

    # Sets color of text
    def TextColor(self, i):

        if i == 0:
            self.setColorIcon(Qt.black)
            self.textBox_1.setTextColor(Qt.black)
            return

        if i == 1:
            self.setColorIcon(Qt.red)
            self.textBox_1.setTextColor(Qt.red)
            return

        if i == 2:
            self.setColorIcon(Qt.green)
            self.textBox_1.setTextColor(Qt.green)
            return

        if i == 3:
            self.setColorIcon(Qt.blue)
            self.textBox_1.setTextColor(Qt.blue)
            return

        if i == 4:
            self.setColorIcon(Qt.yellow)
            self.textBox_1.setTextColor(Qt.yellow)
            return

        if i == 5:
            self.setColorIcon(Qt.gray)
            self.textBox_1.setTextColor(Qt.gray)
            return

        if i == 6:
            self.setColorIcon(Qt.magenta)
            self.textBox_1.setTextColor(Qt.magenta)
            return

        else:
            return

    # Sets the color icon on the QToolBar
    def setColorIcon(self, color):
        pixelMap = QPixmap(48, 24)
        pixelMap.fill(Qt.black)
        painter = QPainter(pixelMap)
        painter.fillRect(4, 4, 40, 16, color)
        painter.end()
        self.colorLabel.setPixmap(pixelMap)

    # Sets the highlight color icon on the QToolBar
    def setHighlightIcon(self, color):
        pixelMap = QPixmap(48, 24)
        pixelMap.fill(Qt.black)
        painter = QPainter(pixelMap)
        painter.fillRect(4, 4, 40, 16, color)
        painter.end()
        self.highlightLabel.setPixmap(pixelMap)

    # Called when the QMainWindow is closed
    def closeEvent(self, event):
        if self.needsSave:
            self.promptSaveMessage()
        if self.saveMessageCancel:
            event.ignore()
        elif self.needsSave:
            self.saveWindow.closeOnSave = True
            event.ignore()

    # Called when any key is pressed
    def keyPressEvent(self, e):
        self.statusBar().clearMessage()

    # Called when text in the AppWidget QTextEdit is changed
    def textEditedEvent(self):
        self.needsSave = True
        self.statusBar().clearMessage()

        # Update current text color and highlight under cursor for color button displays
        self.setColorIcon(self.textBox_1.textColor())
        self.setHighlightIcon(self.textBox_1.textBackgroundColor())

        if not self.Edited:
            self.window_title = self.window_title + " -- Edited"
            self.setWindowTitle(self.window_title)
            self.Edited = True

    # Called when the QTextCursor in the AppWidget QTextEdit is moved
    def cursorMovedEvent(self):

        # Do not update formatting while the user is selecting text
        if not self.textBox_1.textCursor().hasSelection():

            # Update current text color and highlight under cursor for color button displays
            self.setColorIcon(self.textBox_1.textColor())
            self.setHighlightIcon(
                self.textBox_1.textBackgroundColor())

            # Update the current font formatting (bold, italics, underline, etc.)
            self.bold_action.setChecked(
                self.textBox_1.fontWeight() == QFont.Bold)
            self.italic_action.setChecked(
                self.textBox_1.fontItalic())
            self.underline_action.setChecked(
                self.textBox_1.fontUnderline())
            self.aln_right_action.setChecked(
                self.textBox_1.alignment() == Qt.AlignRight)
            self.aln_left_action.setChecked(
                self.textBox_1.alignment() == Qt.AlignLeft)
            self.aln_center_action.setChecked(
                self.textBox_1.alignment() == Qt.AlignCenter)
            self.aln_justify_action.setChecked(
                self.textBox_1.alignment() == Qt.AlignJustify)
            self.fonts.setCurrentFont(self.textBox_1.currentFont())

            if self.textBox_1.fontPointSize() in FONT_SIZES:
                self.fontsize.setCurrentIndex(FONT_SIZES.index(
                    self.textBox_1.fontPointSize()))

    # Opens the file dialog to save a new file or the working file. Returns false if canceled
    def saveNoteSlot(self):

        if self.Edited:
            self.window_title = self.window_title[:-10]
            self.setWindowTitle(self.window_title)
            self.Edited = False

        if not self.saveWindow:
            self.saveWindow = AppSaveWindow(self)
            self.saveWindow.initSaveEvent()

    # Opens the file dialog even if a file is already open. Returns false if canceled
    def saveAsNoteSlot(self):

        if not self.saveWindow:
            self.saveWindow = AppSaveWindow(self)
            self.saveWindow.saveAsEvent()

    def newNoteSlot(self):
        self.openNoteSlot(True)

     # Opens a file (isNew defines if the file is a new, empty file)
    def openNoteSlot(self, isNew=False):

        # New File
        if isNew:

            # Prompt save mesage
            if self.needsSave:
                self.promptSaveMessage()

            if not self.needsSave or self.saveMessageSuccess:
                self.currentFile = ''
                self.textBox_1.clear()
                self.textBox_1.setTextColor(Qt.black)
                self.setColorIcon(Qt.black)
                self.window_title = 'Notepad App - untitled.txt'
                self.setWindowTitle(self.window_title)
                self.needsSave = False
                self.Edited = False

        # Open File
        elif not self.openWindow:
            self.openWindow = AppOpenWindow(self)
            self.openWindow.show()

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

        self.saveMessageCancel = False

        # Save the file and store the result
        if button.text() == '&Yes':
            self.saveMessageSuccess = self.saveEvent()

        # Skip saving the file
        elif button.text() == '&No':
            self.needsSave = False

        else:
            self.saveMessageCancel = True

    # Opens the print dialog
    def printEvent(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialogue = QPrintDialog(printer, self)

        if dialogue.exec_() == QPrintDialog.Accepted:
            self.textBox_1.print_(printer)

    # Opens the image file dialog and inserts an image into the QTextEdit
    def insertImage(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, 'Select an Image', '', 'PNG (*.png);;JPEG (*.jpg *.jpeg)')

        if filePath:

            # Create image directory
            if not os.path.exists('users/' + self.textBox_1.mainWindow.user + '/images'):
                os.makedirs(
                    'users/' + self.textBox_1.mainWindow.user + '/images')

            dest = copyfile(filePath, 'users/' + self.textBox_1.mainWindow.user +
                            '/images/' + os.path.basename(filePath))
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
