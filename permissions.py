import os


class dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


def get_permissions(user):
    account_permissions = []

    try:
        f = open('.permissions', 'r')
    except IOError:
        return account_permissions

    # check every line in .permissions
    for line in f:
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


def add_permission(account, filepath):
    # get all filenames this account can access
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
            f = open('.permissions', 'r+')
            accounts = f.read().splitlines()
        except IOError:
            f = open('.permissions', 'w')

        f.seek(0)

        # for each account username, write all associated permissions
        for cur_account in accounts:
            permission_list = cur_account.split()
            if not permission_list:
                continue
            f.write(permission_list[0] + ' ')
            # if this account in the list is the current account, add permissions from permissions instead of permission_list
            if permission_list[0] == account:
                found_user = True
                for add in permissions:
                    f.write(add + ' ')
            else:
                for permission in permission_list[1:]:
                    f.write(permission + ' ')
            f.write('\n')

        # if this account had no permissions, just add them and this permission to the end of the file
        if not found_user:
            f.write(account + ' ' + fix_path + '\n')

        f.close()
