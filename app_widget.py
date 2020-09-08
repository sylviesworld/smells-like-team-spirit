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
        #self.mainLayout.setContentsMargins(25, 25, 25, 150)
        
        # Create Text box
        self.textBox = QTextEdit()
        self.mainLayout.addWidget(self.textBox)

        # Set main layout to app widget
        self.setLayout(self.mainLayout)
    
    def saveFile(self, fileName):
        f = open(fileName, 'w')
        f.write(self.textBox.toPlainText())
        f.close()
