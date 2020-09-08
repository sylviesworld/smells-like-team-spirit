from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout

class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create main layout to nest new layouts within
        self.mainLayout = QVBoxLayout()
        
        # Create Text box
        self.textBox = QTextEdit()
        self.textBox.setLineWrapMode(QTextEdit.NoWrap)
        self.textBox.setFontPointSize(10)
        self.mainLayout.addWidget(self.textBox)

        # Set main layout to app widget
        self.setLayout(self.mainLayout)
    
    # Creaes a new file or opens an existing and saves the QTextEdit text
    def saveFile(self, fileName):
        f = open(fileName, 'w')
        f.write(self.textBox.toPlainText())
        f.close()

    # Opens file and reads the text to QTextEdit
    def openFile(self, fileName):
        f = open(fileName, 'r')
        self.textBox.setPlainText(f.read())
        f.close()
