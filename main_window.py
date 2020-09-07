#!/usr/bin/python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QDesktopWidget

# this class inherits from QMainWindow and will be used to set up the applications GUI
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # Get screen resolution
        screenBounds = QDesktopWidget().screenGeometry(0)

        self.setWindowTitle('Notepad App')
        self.setGeometry(0, 0, screenBounds.width() * 0.5, screenBounds.height() * 0.6)

        # Center the screen
        rect = self.frameGeometry();
        centerScreen = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(centerScreen)
        self.move(rect.topLeft())

