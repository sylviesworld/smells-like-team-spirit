import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFileSystemModel, QGridLayout, QTreeView, QPushButton, QMessageBox
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QTextCursor
from permissions import check_permission, add_permission
from encrypt_file import decrypt_file

# The window for opening a file
class OpenWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.textEdit = mainWindow.centralWidget.textBox
        self.setWindowTitle('Open File')
        self.resize(1600, 800)
        self.layout = QGridLayout()

        self.openPath = ''

        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(QDir.currentPath() + '/users/')
        
        self.fileTree = QTreeView()
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(self.fileModel.index(QDir.currentPath() + '/users/'))
        self.fileTree.setColumnWidth(0, 500)
        self.fileTree.doubleClicked.connect(self.openEvent)

        self.layout.addWidget(self.fileTree, 0, 0)
    
        openButton = QPushButton('Open')
        openButton.clicked.connect(self.openEvent)
        self.layout.addWidget(openButton, 1, 0)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)
        self.layout.addWidget(cancelButton, 1, 1)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setLayout(self.layout)

    def closeEvent(self, event):
        self.mainWindow.openWindow = None

    # Opens the file selected in the QTreeView
    def openEvent(self):
        
        indexItem = self.fileModel.index(self.fileTree.currentIndex().row(), 0, self.fileTree.currentIndex().parent())
        filePath = self.fileModel.filePath(indexItem)
        # Cannot open directories
        if self.fileModel.isDir(self.fileTree.currentIndex()):
            return

        # Open file dialog
        can_open = check_permission(self.mainWindow.user, filePath)
        if can_open:
                
            self.mainWindow.saveMessageSuccess = False

            # Prompt the user to save the working file
            if self.mainWindow.needsSave:
                self.mainWindow.promptSaveMessage()

            if not self.mainWindow.needsSave or self.mainWindow.saveMessageSuccess:
                self.openFile(filePath)
                self.mainWindow.currentFile = filePath
                self.mainWindow.window_title = f"Notepad App - {os.path.basename(filePath)}"
                self.mainWindow.setWindowTitle(self.mainWindow.window_title)

                # Cursor must be moved to update QTextEdit.textColor member
                self.textEdit.moveCursor(
                    QTextCursor.Right, QTextCursor.MoveAnchor)
                self.mainWindow.setColorIcon(self.textEdit.textColor())
                self.textEdit.moveCursor(
                    QTextCursor.Left, QTextCursor.MoveAnchor)

                self.mainWindow.needsSave = False
                self.mainWindow.Edited = False
                self.close()

        else:
            msg = QMessageBox()
            if self.mainWindow.user != 'None':
                msg.setText(
                    self.mainWindow.user + ' does not have permission to open file: ' + os.path.basename(filePath))
            else:
                msg.setText(
                    'Sign into account to open private file: ' + os.path.basename(filePath))
            msg.exec_()

    # Opens file and reads the text to QTextEdit
    def openFile(self, filePath):
        f = open(filePath, 'rb')
        self.textEdit.setHtml(decrypt_file(f.read()))
        f.close()
