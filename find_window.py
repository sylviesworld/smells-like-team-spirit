from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QGridLayout,  QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5 import QtGui

# The window for finding text in the QTextEdit
class FindWindow(QWidget):
    def __init__(self, textEdit):
        super().__init__()

        self.setWindowTitle('Find')
        self.resize(600, 400)

        # Get QTextEdit through constructor
        self.textEdit = textEdit
        layout = QGridLayout()

        findLabel = QLabel('Find Text: ')
        self.findLineEdit = QLineEdit()
        layout.addWidget(findLabel, 0, 0)
        layout.addWidget(self.findLineEdit, 0, 1)

        self.caseCheck = QCheckBox('Case Sensitive')
        layout.addWidget(self.caseCheck, 1, 0)
        
        # Find is pressed repeatedly to find every occurance
        findButton = QPushButton('Find')
        findButton.clicked.connect(self.findText)
        layout.addWidget(findButton, 1, 1)

        closeButton = QPushButton('Close')
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton, 2, 1)

        self.setLayout(layout)

    # Finds the text, moves the cursor, and selects. Moves to top of document if end is reached
    def findText(self):
        flags = QtGui.QTextDocument.FindFlags()
        
        # Case sensitive flags if checkbox is checked
        if self.caseCheck.isChecked() :
            flags = flags | QtGui.QTextDocument.FindCaseSensitively

        searchText = self.findLineEdit.text().strip()
        
        # Prompt user to search non-empty strings
        if searchText == '':
            self.findMessageBox('Please enter text to search.')
            return False

        r = self.textEdit.find(searchText, flags)
            
        # Search is false if word not found or end of document is reached
        if not r:
            self.textEdit.moveCursor(QtGui.QTextCursor.Start)
            r = self.textEdit.find(searchText, flags)

            if not r :
                self.findMessageBox('Text not found.')
        
        return r

    # Displays find info to the user
    def findMessageBox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle('Find Info')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def createWindow(self):
        self.show()

