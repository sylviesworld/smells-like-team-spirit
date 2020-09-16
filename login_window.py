import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

class SignupWindow(QWidget):
    def create_account(self):
        f = open('note_accounts.txt', 'r')

        num_accounts = int(f.readline())
        num_accounts += 1

        all_file = f.read()
        
        f.close()

        f = open('note_accounts.txt', 'w')
        
        f.write(str(num_accounts) + '\n' + all_file + self.lineEdit_newname.text() + '\n' + self.lineEdit_newpassword.text() + '\n\n')

        f.close()
    
        self.close()
    def __init__(self):
        super().__init__()
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
        self.lineEdit_newpassword.setPlaceholderText('Please enter password')
        layout.addWidget(label_newpassword, 1, 0)
        layout.addWidget(self.lineEdit_newpassword, 1, 1)

        button_create_account = QPushButton('Create account')
        button_create_account.clicked.connect(self.create_account)
        layout.addWidget(button_create_account, 2, 0)

        self.setLayout(layout)

class LoginWindow(QWidget):
    def check_credentials(self):
        #print("Made it to function")

        f = open('note_accounts.txt', 'r')
        num_accounts = int(f.readline())

        f.readline() #reads whitespace between num_accounts and first user/pass pair

        for x in range(num_accounts):
            username = f.readline()
            password = f.readline()
            
            username = username.strip()
            password = password.strip()

            if self.lineEdit_username.text() == username and self.lineEdit_password.text() == password:
                return 'True'
        
            elif self.lineEdit_username.text() == username and self.lineEdit_password.text() != password:
                return 'Wrong pass'

            f.readline() #reads whitespace between current account and next user/pass pair
        
        f.close()

        return 'False'

    def login_result(self):
        msg = QMessageBox()

        result = self.check_credentials()

        if result == 'True':
            msg.setText('Success')
            msg.exec_()
            self.main_window.show()
            self.close()
        
        elif result == 'Wrong pass':
            msg.setText('Incorrect password')
            msg.exec_()
        
        elif result == 'False':
            msg.setText('Username not found')
            msg.exec_()

    def create_account_window(self):
        self.dialog = SignupWindow()
        self.dialog.show()
        
    def __init__(self):
        super().__init__()
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
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        
        button_login = QPushButton('Login')
        button_login.clicked.connect(self.login_result)
        layout.addWidget(button_login, 2, 0)

        button_signup = QPushButton('Sign up')
        button_signup.clicked.connect(self.create_account_window)
        layout.addWidget(button_signup, 2, 1)

        self.setLayout(layout)
