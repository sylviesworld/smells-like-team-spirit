from main_window import*
from account_windows import*
import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication

import unittest

app = QApplication(sys.argv)

class TestPermission(unittest.TestCase):
    # default variables, setup skeleton of app to run tests in
    def setUp(self):
        if not os.path.exists('users/test'):
            os.makedirs('users/test')

        first = False

        # .note_accounts needs to exist and contain test username and password
        try:
            f = open('.note_accounts', 'r')
            first = True
        except IOError:
            f = open('.note_accounts', 'w')
            f.write(encrypt('test') + ' ' + encrypt('password') + ' ' + encrypt('test@test.com') + encrypt('\n'))
            f.close()

        self.main_window = MainWindow()
        self.main_window.user = 'test' 
        self.login_window = LoginWindow()

        self.password_window = ChangePasswordWindow()
        self.password_window.user = 'test'
        
        self.delete_window = DeleteAccountWindow()
        self.delete_window.user = 'test'
        self.delete_window.main_window = self.main_window

        if first:
            f.close()

    # test that check_permission() correctly matches user with their permissions
    # also essentially tests add_permission()
    def testCheckPermission(self):
        # user starts out without access to text.txt
        self.assertFalse(check_permission(self.main_window.user, 'users/test/test.txt'))
        # add the permission
        add_permission(self.main_window.user, 'users/test/test.txt')
        # user now has access so check_permission returns 'True'
        self.assertTrue(check_permission(self.main_window.user, 'users/test/test.txt'))

    # test that change_password() changes the user's password
    def testChangePassword(self):
        # set all variables normally set by a QEditLine input box
        old = 'password'
        new = 'newpassword'
        match = 'newpassword'

        self.login_window.lineEdit_username.setText('test')
        self.login_window.lineEdit_password.setText('password')

        self.password_window.lineEdit_oldpassword.setText(old)
        self.password_window.lineEdit_newpassword.setText(new)
        self.password_window.lineEdit_reenterpassword.setText(match)

        # username and password combo set above is correct
        self.assertEqual(self.login_window.check_credentials(), 'True')
        # change password from what was set above
        self.password_window.change_password()
        # password has changed, so username and password combo from above no longer works
        self.assertEqual(self.login_window.check_credentials(), 'Wrong pass')
       
        # set password variable equal to the newly changed password
        self.login_window.lineEdit_password.setText('newpassword')
        # username and new password combo work
        self.assertEqual(self.login_window.check_credentials(), 'True')
        
    # test that deleting an account also deletes the account's note directory
    def testDeleteAccountDirectory(self):
        # parameter given to delete_account() must have text() == '&Yes' to trigger deleting the directory
        choice = QMessageBox()
        choice.setText('&Yes')
        
        # directory exists before call
        self.assertTrue(os.path.exists('users/test'))
        # delete the account and directory
        self.delete_window.delete_account(choice)
        # directory no longer exists
        self.assertFalse(os.path.exists('users/test'))

    # test encryption and decryption of file contents (string)
    def testEncryptDecryptFile(self):
        original = 'this is a test'
        
        # encrypt the string
        encrypted = encrypt_file(original)
        # encrypted string should not match the original
        self.assertNotEqual(original, encrypted)

        # decrypt the string
        decrypted = decrypt_file(encrypted)
        # decrypted string should match the original
        self.assertEqual(original, decrypted)

    # cleans up leftover files/directories from tests
    def tearDown(self):
        if os.path.exists('users/test'):
            shutil.rmtree('users/test')

        if os.path.exists('.permissions'):
            os.remove('.permissions')
        
        if os.path.exists('.note_accounts'):
            os.remove('.note_accounts')

        if os.path.exists('.key'):
            os.remove('.key')

        return
