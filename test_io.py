from main_window import *
import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication
from encrypt_file import decrypt_file, encrypt_file

import unittest

app = QApplication(sys.argv)


class TestIO(unittest.TestCase):
    """Unit tests for app IO"""

    # Initialize tests
    def setUp(self):

        if not os.path.exists('users/guest'):
            os.makedirs('users/guest')
        if not os.path.exists('test'):
            os.makedirs('test')

        self.mainWindow = MainWindow()
        self.mainWindow.user = 'guest'
        self.mainWindow.currentFile = ''

    # Test if QTextEdit text is saved correctly
    def testSaveFile(self):
        self.mainWindow.saveEvent()
        self.mainWindow.centralWidget.textBox.setText('Hello!')
        self.mainWindow.saveWindow.saveFile('test/hello.txt')
        f = open('test/hello.txt', 'rb')
        self.assertEqual(
            self.mainWindow.centralWidget.textBox.toHtml(), decrypt_file(f.read()))
        f.close()

    # Test if QTextEdit text matches text from file
    def testOpenFile(self):
        self.mainWindow.openEvent(False)
        self.mainWindow.centralWidget.textBox.setText('Goodbye!')
        goodbyeText = self.mainWindow.centralWidget.textBox.toHtml()
        self.mainWindow.centralWidget.textBox.clear()
        f = open('test/goodbye.txt', 'wb')
        f.write(encrypt_file(goodbyeText))
        f.close()
        self.mainWindow.openWindow.openFile('test/goodbye.txt')
        self.assertEqual(
            self.mainWindow.centralWidget.textBox.toHtml(), goodbyeText)

    # Test if note group folder was successfully created
    def testCreateGroup(self):
        self.mainWindow.createGroupEvent()
        self.mainWindow.groupWindow.createFolder('test/subtest')
        self.assertTrue(os.path.exists('test/subtest'))

    # Test if save window closes successfully
    def testSaveWindowClose(self):
        self.mainWindow.saveEvent()
        self.mainWindow.saveWindow.close()
        self.assertEqual(self.mainWindow.saveWindow, None)

    # Test if open window closes successfully
    def testOpenWindowClose(self):
        self.mainWindow.openEvent(False)
        self.mainWindow.openWindow.close()
        self.assertEqual(self.mainWindow.openWindow, None)

    # Test if group window closes successfully
    def testGroupWindowClose(self):
        self.mainWindow.createGroupEvent()
        self.mainWindow.groupWindow.close()
        self.assertEqual(self.mainWindow.groupWindow, None)

    # Clean up the test files
    def tearDown(self):
        shutil.rmtree('test')
        return
