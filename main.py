#!/usr/bin/python3

import sys
import os
from main_window import MainWindow
from account_windows import LoginWindow
from PyQt5.QtWidgets import QApplication


def main():

    # placeholder stylesheet
    stylesheet = """

    QTextEdit {
        background-color: white;
    }

    MainWindow {
        background-color: white;
    }

    """

    # Declare an instance of the application
    app_example = QApplication(sys.argv)
    app_example.setStyleSheet(stylesheet)

    # Create default directory
    if not os.path.exists('users/guest'):
        os.makedirs('users/guest')
    
    login_window = LoginWindow()
    login_window.show()

    # Create main window
    main_window = MainWindow()
    login_window.main_window = main_window

    # This triggers the event loop for the application
    # Calling it inside sys.exit() just ensures a leak free exit
    sys.exit(app_example.exec_())


if __name__ == '__main__':
    main()
