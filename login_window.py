# creation of windows is from PyQt5 tutorial on YouTube by Jie Jenn "PyQt5 Tutorial | Create a simple login form"

import sys
import os
from encrypt import encrypt, decrypt, encrypt_email
from email_server import send_email
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

# class containing functions that open and operate a separate window for creating an account

class SignupWindow(QWidget): 
    # for checking if signup info is valid, sets label text for each error
    def legal_account(self, username, password, email):
        illegal_chars = [' ', '`', '~', '[', ']', '{', '}', '(', ')', ';', ':', '\'', '"', ',', '<', '>', '/', '?', '\\', '|']
        legal = True
        empty = False
        
        user_error = self.label_userError
        password_error = self.label_passwordError
        email_error = self.label_emailError

        # reset error message to blank before checking each attempt to submit info
        user_error.setText('')
        password_error.setText('')
        email_error.setText('')

        # for checking if username is already taken
        try:
            f = open('.note_accounts', 'r')
        except IOError:
            empty = True

        if not empty:
            for line in f:
                account_info = line.split()
                account_name = decrypt(account_info[0])
                if account_name == username:
                    user_error.setText('Username already taken')
                    legal = False
                    break

        # no field can be left blank
        if username == '':
            user_error.setText('Username cannot be blank')
            legal = False
        if password == '':
            password_error.setText('Password cannot be blank')
            legal = False
        if email == '':
            email_error.setText('Email cannnot be blank')
            legal = False

        # check each field against illegal characters
        for c in illegal_chars:
            if username.find(c) != -1:
                user_error.setText('Username cannot contain "' + c + '"')
                legal = False
            if password.find(c) != -1:
                password_error.setText('Password cannot contain "' + c + '"')
                legal = False
            if email.find(c) != -1:
                email_error.setText('Email cannot contain "' + c + '"')
                legal = False

        # check email format
        if email.find('@') <= 0 or (email.find('.com') == -1 and email.find('.gov') == -1 and email.find('.edu') == -1 and email.find('.net') == -1):
            email_error.setText('Email must have format: user@address.xxx')
            legal = False

        return legal

    # reads in all currently existing accounts, encrypts user/pass, writes new file
    def create_account(self):
        username = self.lineEdit_newuser.text()
        password = self.lineEdit_newpassword.text()
        email = self.lineEdit_email.text()

        if not self.legal_account(username, password, email):
            return

        all_file = ''
        try:
            f = open('.note_accounts', 'r+')
            all_file = f.read()
        except IOError:
            f = open('.note_accounts', 'w')

        f.seek(0)
        
        # does encryption on new username and password (see encrypt.py)
        e_user = encrypt(username)
        e_pass = encrypt(password)

        # encrypts email name and address
        encrypted_email = encrypt_email(email)

        f.write(all_file + e_user + ' ' + e_pass + ' ' + encrypted_email[0] + ' ' + encrypted_email[1] + '\n')

        f.close()

        # sends a confirmation email to the email used to sign up
        send_email(email)

        # Make directory for user
        if not os.path.exists('users/' + username):
            os.makedirs('users/' + username)

        self.close()

    def __init__(self):
        super().__init__()
        # from YouTube tutorial
        self.setWindowTitle('Signup window')
        self.resize(800, 240)

        layout = QGridLayout()

        label_newuser = QLabel('<font size="4"> Username: </font>')
        self.label_userError = QLabel('')
        self.label_userError.setStyleSheet("color: red;")
        self.lineEdit_newuser = QLineEdit()
        self.lineEdit_newuser.setPlaceholderText('Please enter username')
        layout.addWidget(label_newuser, 0, 0)
        layout.addWidget(self.lineEdit_newuser, 0, 1)
        layout.addWidget(self.label_userError, 1, 1)

        label_newpassword = QLabel('<font size="4"> Password: </font>')
        self.label_passwordError = QLabel('')
        self.label_passwordError.setStyleSheet("color: red;")
        self.lineEdit_newpassword = QLineEdit()
        self.lineEdit_newpassword.setEchoMode(QLineEdit.Password)
        self.lineEdit_newpassword.setPlaceholderText('Please enter password')
        layout.addWidget(label_newpassword, 2, 0)
        layout.addWidget(self.lineEdit_newpassword, 2, 1)
        layout.addWidget(self.label_passwordError, 3, 1)

        label_email = QLabel('<font size="4"> Email: </font>')
        self.label_emailError = QLabel('')
        self.label_emailError.setStyleSheet("color: red;")
        self.lineEdit_email = QLineEdit()
        self.lineEdit_email.setPlaceholderText('Please enter email')
        layout.addWidget(label_email, 4, 0)
        layout.addWidget(self.lineEdit_email, 4, 1)
        layout.addWidget(self.label_emailError, 5, 1)
        
        button_create_account = QPushButton('Create account')
        button_create_account.clicked.connect(self.create_account)
        layout.addWidget(button_create_account, 6, 1)

        self.setLayout(layout)

# class containing functions that open and operate first window when starting app, for logging in

class LoginWindow(QWidget):
    # reads in accounts from file and checks if entered user/pass pair matches any existing
    def check_credentials(self):
        try:
            f = open('.note_accounts', 'r')
        except IOError:
            return 'False'
        
        # check every account until a matching username is found or entire file is searched
        for line in f:
            cur_user = line.split()

            username = decrypt(cur_user[0])
            password = decrypt(cur_user[1])

            # checks for account's existence as well as correct password for outputting appropriate message
            if self.lineEdit_username.text() == username and self.lineEdit_password.text() == password:
                self.user = self.lineEdit_username.text()

                # Create user directory
                if not os.path.exists('users/' + self.user):
                    os.makedirs('users/' + self.user)

                return 'True'

            elif self.lineEdit_username.text() == username and self.lineEdit_password.text() != password:
                return 'Wrong pass'

        f.close()

        return 'False'

    # handles actual output message based on results of check_credentials()
    def login_result(self):
        msg = QMessageBox()

        result = self.check_credentials()

        # opens note app and closes login window
        if result == 'True':
            self.main_window.show()
            self.main_window.user = self.user
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
    
    # for opening main window if no account is used
    def bypass(self):
        self.main_window.show()
        self.main_window.user = self.user
        
        # Create guest directory
        if not os.path.exists('users/guest'):
            os.makedirs('users/guest')

        self.close()

    def __init__(self):
        super().__init__()
        # from YouTube tutorial
        self.user = "guest"
        self.setWindowTitle('Login Window')
        self.resize(600, 120)

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

        button_noaccount = QPushButton('Continue without account')
        button_noaccount.clicked.connect(self.bypass)
        layout.addWidget(button_noaccount, 3, 0, 3, 0)

        self.setLayout(layout)
