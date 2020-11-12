"""The example code from Prof. Henley's Unit Test Lecture.
Not used in the Note app -- only for reference"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import unittest


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 400, 200, 200)
        self.textbox = QLineEdit(self)
        self.textbox.move(2, 2)
        self.button = QPushButton("Go Vols!", self)
        self.button.move(15, 20)
        self.button.clicked.connect(self.onClick)
        self.show()

    def onClick(self):
        cleanedText = removeSpaces(self.textbox.text())
        QMessageBox.question(self, "", cleanedText,
                             QMessageBox.Ok, QMessageBox.Ok)


# Utility Functions
class CleanUtility:
    def removeSpaces(self, str):
        return str.replace(' ', '')

    def removeNumbers(self, str):
        return ''.join(filter(lambda chr: not chr.isdigit(), str))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


# Unit Tests
class TestCleaningMethods(unittest.TestCase):
    def setUp(self):
        self.cleaner = CleanUtility()

    def test_removeSpaces(self):
        self.assertEqual(self.cleaner.removeSpaces("a b c"), "abc")
        self.assertLess(
            len(self.cleaner.removeSpaces("foo bar")), len("foo bar"))

    def test_removeNumbers(self):
        self.assertEqual(self.cleaner.removeNumbers("a1b2c3"), "abc")
