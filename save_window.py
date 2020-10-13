from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QPrinter)
from PyQt5 import QtGui

# The window for saving a file

class SaveWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowTitle('Save As')
        self.resize(600, 400)

        # Get AppWidget through constructor
        self.mainWindow = mainWindow
        self.textEdit = mainWindow.centralWidget.textBox
        layout = QGridLayout()

        fnLabel = QLabel('File name: ')
        self.fnLineEdit = QLineEdit()
        layout.addWidget(fnLabel, 0, 0)
        layout.addWidget(self.fnLineEdit, 0, 1)

        typeLabel = QLabel('Save as type: ')
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem('Text Files (*.txt)')
        self.typeComboBox.addItem('PDF Files (*.pdf)')

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.saveEvent)
        layout.addWidget(saveButton, 1, 1)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)
        layout.addWidget(cancelButton, 2, 1)

        self.setLayout(layout)

    # Displays confirm save message to the user
    def confirmMessageBox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle('Confirm Save As')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.saveMessageEvent)
        msg.exec_()

    # Displays generic save message to the user
    def saveMessageBox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle('Save Info')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # Handles the response to the confirm message box
    def confirmMessageEvent(self, button):

        if button.text() == '&Yes':
            #self.saveMessageSuccess = self.saveEvent()

        # Skip saving the file
        elif button.text() == '&No':
            #self.needsSave = False

        else:
            return

    def createWindow(self):
        self.show()

    def saveEvent(self):
        if self.currentFile == '':

            fileName, extension = os.path.splitext(self.fnLabel.text())
            filePath = 'users/' + self.mainWindow.user + '/' + fileName

            # Save text file
            if self.typeComboBox.currentIndex() == 0:
                filePath += '.txt'
                self.saveFile(filePath)
                self.mainWindow.currentFile = filePath
                self.mainWindow.statusBar().showMessage('File saved.')
                self.mainWindow.needsSave = False
                self.mainWindow.window_title = 'Notepad App - {os.path.basename(filePath)}'
                self.mainWindow.setWindowTitle(self.mainWindow.window_title)
                self.mainWindow.add_permission(self.mainWindow.user, fileName + '.txt')

            # Save PDF
            else:
                filePath += '.pdf'
                self.savePDF(filePath)
                self.mainWindow.add_permission(self.user, fileName + '.pdf')

        else:
            self.saveFile(self.mainWindow.currentFile)
            self.mainWindow.statusBar().showMessage('File saved.')
            self.mainWindow.needsSave = False
            self.mainWindow.add_permission(self.mainWindow.user, os.path.basename(self.mainWindow.currentFile))

    # Creaes a new file or opens an existing and saves the QTextEdit text
    def saveFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.textEdit.toHtml())
        f.close()

    # Saves the file as a PDF
    def savePDF(self, filePath):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(fileName)
        self.centralWidget.textBox.document().print_(printer)

