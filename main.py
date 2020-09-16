#!/usr/bin/python3

import sys
from main_window import MainWindow
from login_window import LoginWindow
from PyQt5.QtWidgets import QApplication

def main():

    # Declare an instance of the application
    app_example = QApplication(sys.argv)
    
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
