"""Encrypt and decrypt files"""


from cryptography.fernet import Fernet
import sys


def generate_key():
    key = Fernet.generate_key()

    f = open('.key', 'wb')
    f.write(key)
    f.close()


def encrypt_file(original):
    try:
        f = open('.key', 'rb')
    except IOError:
        generate_key()
        f = open('.key', 'rb')

    key = f.read()
    f.close()

    original = original.encode('utf8')
    fern = Fernet(key)

    return fern.encrypt(original)


def decrypt_file(encrypted):
    try:
        f = open('.key', 'rb')
    except IOError:
        print('error: no key')
        sys.exit()

    key = f.read()
    f.close()

    fern = Fernet(key)

    return fern.decrypt(encrypted).decode('utf8')
