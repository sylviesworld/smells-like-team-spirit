from PyQt5.QtWidgets import QWidget, QFileSystemModel, QGridLayout, QTreeView, QPushButton
from PyQt5.QtCore import QDir

# The window for opening a file
class OpenWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Open File')
        self.resize(600, 400)
        self.layout = QGridLayout()

        self.openPath = ''

        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(QDir.currentPath() + '/users/')
        
        self.fileTree = QTreeView()
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(self.fileModel.index(QDir.currentPath() + '/users/'))

        self.layout.addWidget(self.fileTree, 0, 0)
    
        openButton = QPushButton('Open')
        openButton.clicked.connect(self.openEvent)
        layout.addWidget(openButton, 1, 0)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.closeWindow)
        layout.addWidget(cancelButton, 1, 1)

        self.setLayout(self.layout)

    def openEvent(self):
        return
