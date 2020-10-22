from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFileDialog
from find_window import FindWindow
import os
import uuid
from shutil import copyfile

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']
HTML_EXTENSIONS = ['.htm', '.html']


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create main layout to nest new layouts within
        self.mainLayout = QVBoxLayout()

        # Create Text box
        self.textBox = TextEdit()
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
        filePath, _ = QFileDialog.getOpenFileName(
            self, 'Select an Image', '', 'PNG (*.png);;JPEG (*.jpg *.jpeg)')

        if filePath:

            # Create image directory
            if not os.path.exists('users/' + self.textBox.mainWindow.user + '/images'):
                os.makedirs(
                    'users/' + self.textBox.mainWindow.user + '/images')

            dest = copyfile(filePath, 'users/' + self.textBox.mainWindow.user +
                            '/images/' + os.path.basename(filePath))
            self.textBox.textCursor().insertImage(dest)


def hexuuid():
    return uuid.uuid4().hex


def splitext(p):
    return os.path.splitext(p)[1].lower()


class TextEdit(QTextEdit):

    #AutoBulletList()

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():

            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)

                    # Create image directory
                    if not os.path.exists('users/' + self.mainWindow.user + '/images'):
                        os.makedirs(
                            'users/' + self.mainWindow.user + '/images')

                    dest = copyfile(u.toLocalFile(
                    ), 'users/' + self.mainWindow.user + '/images/' + os.path.basename(u.toLocalFile()))
                    cursor.insertImage(dest)
                else:
                    break

            else:
                return

        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)
