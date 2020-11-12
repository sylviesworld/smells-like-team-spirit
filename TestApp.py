import sys
import os
import shutil
import unittest
from app import *
from PyQt5.QtWidgets import QApplication
from encrypt_file import decrypt_file, encrypt_file

app = QApplication(sys.argv)

class TestApp(unittest.TestCase):
    
    # Initialize tests
    def setUp(self):

        if not os.path.exists('users/admin'):
            os.makedirs('users/admin')
        if not os.path.exists('unittest'):
            os.makedirs('unittest')

        self.mainWindow = MainWindow()
        self.mainWindow.user = 'admin'
        self.mainWindow.currentFile = ''

    # Test save slot
    def testSaveSlot(self):
        self.mainWindow.saveNoteSlot()
        self.mainWindow.textBox_1.setText('Test!')
        self.mainWindow.saveWindow.saveFile('unittest/test.txt')
        f = open('unittest/test.txt', 'rb') 
        self.assertEqual(self.mainWindow.textBox_1.toHtml(), decrypt_file(f.read()))
        f.close()

    # Test open slot
    def testOpenSlot(self):
        self.mainWindow.openNoteSlot()
        self.mainWindow.textBox_1.setText('Test 2')
        test2file = self.mainWindow.textBox_1.toHtml()
        self.mainWindow.textBox_1.clear()
        f = open('unittest/test2.txt', 'wb')
        f.write(encrypt_file(test2file))
        f.close()
        self.mainWindow.openWindow.openFile('unittest/test2.txt')
        self.assertEqual(self.mainWindow.textBox_1.toHtml(), test2file)

    # Test new note slot
    def testNewNoteSlot(self):
        self.mainWindow.saveNoteSlot()
        self.mainWindow.textBox_1.setText("Testing clear")
        self.mainWindow.needsSave = False
        self.mainWindow.newNoteSlot()
        self.assertEqual(self.mainWindow.textBox_1.toPlainText(), "")
    
    # Remove unittest dir
    def tearDown(self):
        shutil.rmtree('unittest')
        return