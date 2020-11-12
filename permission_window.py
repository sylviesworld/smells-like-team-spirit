from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QFormLayout, QGridLayout,
                             QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox)
from PyQt5 import QtGui
from PyQt5 import QtCore
from permissions import check_permission, add_permission
import os


class PermissionWindow(QWidget):
    """The window for giving another user access to a file"""

    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowTitle('Give User Permissions')
        self.resize(600, 100)
        self.mainWindow = mainWindow
        layout = QFormLayout()

        self.userBox = QComboBox()

        for name in os.listdir('users/'):
            if name != self.mainWindow.user and not check_permission(name, self.mainWindow.currentFile):
                self.userBox.addItem(name)

        layout.addRow('Choose User:', self.userBox)

        gridLayout = QGridLayout()
        addButton = QPushButton('Add User')
        addButton.clicked.connect(self.addUser)
        gridLayout.addWidget(addButton, 0, 0)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)
        gridLayout.addWidget(cancelButton, 1, 0)

        layout.addRow(gridLayout)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.mainWindow.permissionWindow = None

    # Adds a user to the current file
    def addUser(self):
        if self.userBox.count() == 0:
            return

        add_permission(self.userBox.currentText(), self.mainWindow.currentFile)
        self.close()
