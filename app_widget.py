from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFileDialog
from find_window import FindWindow

class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create main layout to nest new layouts within
        self.mainLayout = QVBoxLayout()

        # Create Text box
        self.textBox = QTextEdit()
        self.mainLayout.addWidget(self.textBox)

        # Create find window
        self.findWindow = FindWindow(self.textBox)

        # Set main layout to app widget
        self.setLayout(self.mainLayout)

    # Creaes a new file or opens an existing and saves the QTextEdit text
    def saveFile(self, fileName):
        f = open(fileName, 'w')
        f.write(self.textBox.toHtml())
        f.close()

    # Opens file and reads the text to QTextEdit
    def openFile(self, fileName):
        f = open(fileName, 'r')
        self.textBox.setHtml(f.read())
        f.close()

    # Opens the image file dialog and inserts an image into the QTextEdit
    def insertImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Select an Image', '', 'PNG (*.png);;JPEG (*.jpg *.jpeg)')

        if filePath:
            self.textBox.textCursor().insertImage(filePath)

