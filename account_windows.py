# creation of windows is from PyQt5 tutorial on YouTube by Jie Jenn "PyQt5
# Tutorial | Create a simple login form"

import sys
import os
import shutil
from encrypt_account import encrypt, decrypt
from encrypt_file import encrypt_file, decrypt_file
from email_server import send_email
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)


# class containing functions that open and operate a separate window for
# creating an account
class SignupWindow(QWidget):
    # for checking if signup info is valid, sets label text for each error
    def legal_account(self, username, password, email):
        illegal_chars = [' ', '`', '~', '[', ']',
                         '{', '}', '(', ')', ';', ':', '\'', '"', ',', '<', '>', '/', '?', '\\', '|']
        legal = True
        empty = False

        user_error = self.label_userError
        password_error = self.label_passwordError
        email_error = self.label_emailError

        # reset error message to blank before checking each attempt to submit
        # info
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

                if not account_info:
                    continue

                if decrypt(username, account_info[0]):
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
        if email.find('@') <= 0 or (email.find('.com') == -1 and email.find('.gov') ==
                                    -1 and email.find('.edu') == -1 and email.find('.net') == -1):
            email_error.setText('Email must have format: user@address.xxx')
            legal = False

        return legal

    # reads in all currently existing accounts, encrypts user/pass, writes new
    # file
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

        # does encryption on new username, password, and email
        e_user = encrypt(username)
        e_pass = encrypt(password)
        e_email = encrypt(email)

        f.write(all_file + e_user + ' ' + e_pass + ' ' + e_email + '\n')

        f.close()

        msg = QMessageBox()
        msg.setText(
            f'<center>Welcome, {username}</center>\n<center>Thanks for signing up!</center>')
        msg.setWindowTitle('Welcome!')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

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


# class containing functions that open and operate first window when
# starting app, for logging in
class LoginWindow(QWidget):
    # reads in accounts from file and checks if entered user/pass pair matches
    # any existing
    def check_credentials(self):
        try:
            f = open('.note_accounts', 'r')
        except IOError:
            return 'False'

        # check every account until a matching username is found or entire file
        # is searched
        for line in f:
            cur_user = line.split()

            username = decrypt(self.lineEdit_username.text(), cur_user[0])
            password = decrypt(self.lineEdit_password.text(), cur_user[1])

            # checks for account's existence as well as correct password for
            # outputting appropriate message
            if username and password:
                self.user = self.lineEdit_username.text()

                # Create user directory
                if not os.path.exists('users/' + self.user):
                    os.makedirs('users/' + self.user)

                return 'True'

            elif username and not password:
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

class ChangePasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Change password')
        self.resize(800, 240)

        layout = QGridLayout()

        label_oldpassword = QLabel('<font size="4"> Current password: </font>')
        self.label_badold = QLabel('')
        self.label_badold.setStyleSheet("color: red;")
        self.lineEdit_oldpassword = QLineEdit()
        self.lineEdit_oldpassword.setPlaceholderText('Enter current password')
        self.lineEdit_oldpassword.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_oldpassword, 0, 0)
        layout.addWidget(self.lineEdit_oldpassword, 0, 1)
        layout.addWidget(self.label_badold, 1, 1)

        label_newpassword = QLabel('<font size="4"> New password: </font>')
        self.label_badpass = QLabel('')
        self.label_badpass.setStyleSheet("color: red;")
        self.lineEdit_newpassword = QLineEdit()
        self.lineEdit_newpassword.setPlaceholderText('Enter new password')
        self.lineEdit_newpassword.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_newpassword, 2, 0)
        layout.addWidget(self.lineEdit_newpassword, 2, 1)
        layout.addWidget(self.label_badpass, 3, 1)

        label_reenterpassword = QLabel('<font size="4"> Reenter password: </font>')
        self.label_nomatch = QLabel('')
        self.label_nomatch.setStyleSheet("color: red;")
        self.lineEdit_reenterpassword = QLineEdit()
        self.lineEdit_reenterpassword.setPlaceholderText('Reenter password')
        self.lineEdit_reenterpassword.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_reenterpassword, 4, 0)
        layout.addWidget(self.lineEdit_reenterpassword, 4, 1)
        layout.addWidget(self.label_nomatch, 5, 1)

        button_confirm = QPushButton('Confirm')
        button_confirm.clicked.connect(self.change_password)
        layout.addWidget(button_confirm, 6, 1)

        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.close)
        layout.addWidget(button_cancel, 6, 0)

        self.setLayout(layout)

    def change_password(self):
        illegal_chars = [' ', '`', '~', '[', ']', '{', '}', '(', ')', ';', ':', '\'', '"', ',', '<', '>', '/', '?', '\\', '|']
        
        legal = True
        can_change = True

        old_error = self.label_badold
        new_error = self.label_badpass
        match_error = self.label_nomatch

        old_error.setText('')
        new_error.setText('')
        match_error.setText('')

        try:
            f = open('.note_accounts', 'r')
        except IOError:
            old_error.setText('No accounts exist')
            return
        
        old = self.lineEdit_oldpassword.text()
        new = self.lineEdit_newpassword.text()
        match = self.lineEdit_reenterpassword.text()
        
        found = False

        for line in f:
            cur_account = line.split()

            if decrypt(self.user, cur_account[0]):
                found = True
                email = cur_account[2]
                break

        f.close()

        if found:
            if not decrypt(old, cur_account[1]):
                old_error.setText('Incorrect password')
                can_change = False
        else:
            old_error.setText('Account does not exist')
            can_change = False

        if new == '':
            new_error.setText('Password cannot be blank')
            legal = False

        for c in illegal_chars:
            if new.find(c) != -1:
                new_error.setText('Password cannot contain "' + c + '"')
                legal = False

        if new != match:
            match_error.setText('Passwords do not match')
            legal = False

        if legal:
            f = open('.note_accounts', 'r+')

            all_file = f.read()
            
            f.seek(0)

            for line in all_file.splitlines():
                cur_account = line.split()

                if not decrypt(self.user, cur_account[0]):
                    f.write(line + '\n')

            f.write(encrypt(self.user) + ' ' + encrypt(new) + ' ' + email + '\n')

            f.close()

            self.close()

class DeleteAccountWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete account')
        self.resize(600, 120)

        layout = QGridLayout()

        label_password = QLabel('<font size="4"> Password: </font>')
        self.label_incorrectpass = QLabel('')
        self.label_incorrectpass.setStyleSheet("color: red;")
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password, 0, 0)
        layout.addWidget(self.lineEdit_password, 0, 1)
        layout.addWidget(self.label_incorrectpass, 1, 1)

        button_confirm = QPushButton('Confirm')
        button_confirm.clicked.connect(self.prompt_delete_account)
        layout.addWidget(button_confirm, 2, 1)

        button_cancel = QPushButton('Cancel')
        button_cancel.clicked.connect(self.close)
        layout.addWidget(button_cancel, 2, 0)

        self.setLayout(layout)

    def prompt_delete_account(self):
        password = self.lineEdit_password.text()
        legal = True
        self.label_incorrectpass.setText('')
        
        try:
            f = open('.note_accounts', 'r')
        except IOError:
            return

        for line in f:
            cur_account = line.split()

            if decrypt(self.user, cur_account[0]):
                if not decrypt(password, cur_account[1]):
                    self.label_incorrectpass.setText('Incorrect password')
                    legal = False
                    break
        
        f.close()

        if legal:
            msg = QMessageBox()
            msg.setText('Are you sure you want to delete your account? This action will also delete all of your files.')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.buttonClicked.connect(self.delete_account)
            msg.exec_()

    def delete_account(self, button):
        password = self.lineEdit_password.text()

        if button.text() == '&Yes':
            try:
                f = open('.note_accounts', 'r+')
            except IOError:
                return
            
            all_file = f.read()

            f.seek(0)
            
            f.truncate(0)

            for line in all_file.splitlines():
                cur_account = line.split()

                if not decrypt(self.user, cur_account[0]):
                    f.write(line + '\n')

            f.close()

            exists = True

            try:
                f = open('.permissions', 'rb+')
            except IOError:
                exists = False

            if exists:
                all_permissions = decrypt_file(f.read())
                new_file = ''
                
                f.seek(0)

                f.truncate(0)

                for line in all_permissions.splitlines():
                    cur_account = line.split()

                    if cur_account[0] != self.user:
                        new_file += (line + '\n')

                f.write(encrypt_file(new_file))

                f.close()

            shutil.rmtree('users/' + self.user)

            self.close()
            self.main_window.close()
