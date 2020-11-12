import os
from encrypt_file import encrypt_file, decrypt_file


class dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


# get permissions for the user
def get_permissions(user):
    account_permissions = []

    try:
        f = open('.permissions', 'rb')
    except IOError:
        return account_permissions

    decrypted = decrypt_file(f.read())

    # check every line in .permissions
    for line in decrypted.splitlines():
        account = line.split()
        if not account:
            continue
        cur_user = account[0]
        if cur_user == user or cur_user == 'guest':
            for permission in account[1:]:
                account_permissions.append(permission)

    f.close()

    return account_permissions


# check all files that this account can access, compare to given filename
def check_permission(account, fullpath):
    permissions = get_permissions(account)

    short = fullpath.find('users')
    shortpath = fullpath[short:]

    fix_path = ''

    for c in shortpath:
        if c == ' ':
            new_c = '_'
            fix_path += new_c
        else:
            fix_path += c

    for cur_path in permissions:
        if cur_path == fix_path:
            return True

    return False


# get all filenames this account can access
def add_permission(account, filepath):
    permissions = get_permissions(account)

    fix_path = ''

    for c in filepath:
        if c == ' ':
            new_c = '_'
            fix_path += new_c
        else:
            fix_path += c

    # if account doesn't already have access to file, add it to account's permissions
    if fix_path not in permissions:
        found_user = False
        permissions.append(fix_path)

        accounts = []

        # if .permissions doesn't exist, create it
        try:
            f = open('.permissions', 'rb+')
            accounts = decrypt_file(f.read()).splitlines()
        except IOError:
            f = open('.permissions', 'wb')

        f.seek(0)

        # for each account username, write all associated permissions
        for cur_account in accounts:
            permission_list = cur_account.split()
            if not permission_list:
                continue
            byte = (permission_list[0] + ' ').encode('utf-8')
            f.write(byte)
            # if this account in the list is the current account, add permissions from permissions instead of permission_list
            if permission_list[0] == account:
                found_user = True
                for add in permissions:
                    byte = (add + ' ').encode('utf-8')
                    f.write(byte)
            else:
                for permission in permission_list[1:]:
                    byte = (permission + ' ').encode('utf-8')
                    f.write(byte)
            f.write('\n'.encode('utf-8'))

        # if this account had no permissions, just add them and this permission to the end of the file
        if not found_user:
            byte = (account + ' ' + fix_path + '\n').encode('utf-8')
            f.write(byte)

        f.close()

        f = open('.permissions', 'rb+')

        encrypted = encrypt_file(f.read().decode('utf-8'))
        f.seek(0)
        f.write(encrypted)
        f.close()
