# creation of windows is from PyQt5 tutorial on YouTube by Jie Jenn "PyQt5 Tutorial | Create a simple login form"

import sys
from encrypt import do_encryption
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

filename = '.note_accounts'

# class containing functions that open and operate a separate window for creating an account


class SignupWindow(QWidget):
    # reads in all currently existing accounts, encrypts user/pass, writes new file
    def create_account(self):
        f = open(filename, 'r')

        num_accounts = int(f.readline())
        num_accounts += 1

        all_file = f.read()

        f.close()

        # does encryption on new username and password (see encrypt.py)
        encrypted_pair = do_encryption(
            self.lineEdit_newname.text(), self.lineEdit_newpassword.text())

        f = open(filename, 'w')

        f.write(str(num_accounts) + '\n' + all_file +
                encrypted_pair[0] + '\n' + encrypted_pair[1] + '\n\n')

        f.close()

        self.close()

    def __init__(self):
        super().__init__()
        # from YouTube tutorial
        self.setWindowTitle('Signup window')
        self.resize(500, 120)

        layout = QGridLayout()

        label_newname = QLabel('<font size="4"> Username: </font>')
        self.lineEdit_newname = QLineEdit()
        self.lineEdit_newname.setPlaceholderText('Please enter username')

        layout.addWidget(label_newname, 0, 0)
        layout.addWidget(self.lineEdit_newname, 0, 1)

        label_newpassword = QLabel('<font size="4"> Password: </font>')
        self.lineEdit_newpassword = QLineEdit()
        self.lineEdit_newpassword.setEchoMode(QLineEdit.Password)
        self.lineEdit_newpassword.setPlaceholderText('Please enter password')
        layout.addWidget(label_newpassword, 1, 0)
        layout.addWidget(self.lineEdit_newpassword, 1, 1)

        button_create_account = QPushButton('Create account')
        button_create_account.clicked.connect(self.create_account)
        layout.addWidget(button_create_account, 2, 1)

        self.setLayout(layout)

# class containing functions that open and operate first window when starting app, for logging in


class LoginWindow(QWidget):
    # reads in accounts from file and checks if entered user/pass pair matches any existing
    def check_credentials(self):
        f = open(filename, 'r')
        num_accounts = int(f.readline())

        f.readline()  # reads whitespace between num_accounts and first user/pass pair

        # check every account until a matching username is found or entire file is searched
        for x in range(num_accounts):
            username = f.readline()
            password = f.readline()

            username = username.strip()
            password = password.strip()

            # do encryption on entered user/pass to compare to encrypted accounts in file
            encrypted_pair = do_encryption(
                self.lineEdit_username.text(), self.lineEdit_password.text())

            # checks for account's existence as well as correct password for outputting appropriate message
            if encrypted_pair[0] == username and encrypted_pair[1] == password:
                return 'True'

            elif encrypted_pair[0] == username and encrypted_pair[1] != password:
                return 'Wrong pass'

            f.readline()  # reads whitespace between current account and next user/pass pair

        f.close()

        return 'False'

    # handles actual output message based on results of check_credentials()
    def login_result(self):
        msg = QMessageBox()

        result = self.check_credentials()

        # opens note app and closes login window
        if result == 'True':
            msg.setText('Success')
            msg.exec_()
            self.main_window.show()
            self.close()

        # account exists but password is wrong
        elif result == 'Wrong pass':
            msg.setText('Incorrect password')
            msg.exec_()

        # account doesn't exist
        elif result == 'False':
            msg.setText('Username not found')
            msg.exec_()

    def create_account_window(self):
        self.dialog = SignupWindow()
        self.dialog.show()

    def __init__(self):
        super().__init__()
        # from YouTube tutorial
        self.setWindowTitle('Login Window')
        self.resize(500, 120)

        layout = QGridLayout()

        label_name = QLabel('<font size="4"> Username: </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password: </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.login_result)
        layout.addWidget(button_login, 2, 1)

        button_signup = QPushButton('Sign up')
        button_signup.clicked.connect(self.create_account_window)
        layout.addWidget(button_signup, 2, 0)

        self.setLayout(layout)
