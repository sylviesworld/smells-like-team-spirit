#!/usr/bin/python3

import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication

def main():

    # Declare an instance of the application
    app_example = QApplication(sys.argv)
    
    # Create main window
    main_window = MainWindow()
    main_window.show()

    # This triggers the event loop for the application
    # Calling it inside sys.exit() just ensures a leak free exit
    sys.exit(app_example.exec_())
    
if __name__ == '__main__':
    main()
