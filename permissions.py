import os
from encrypt import dictionary

def get_permissions(user):
    f = open('.permissions', 'r')

    account_permissions = []

    for line in f:
        account = line.split()
        if not account:
            continue
        cur_user = account[0];
        if cur_user == user or cur_user == 'None':
            for permission in account[1:]:
                account_permissions.append(permission)

    f.close()

    return account_permissions

def check_permission(account, filename):
    permissions = get_permissions(account)

    for cur_file in permissions:
        if cur_file == filename:
            return True

    return False

def add_permission(account, filename):
    permissions = get_permissions(account)
    
    if filename not in permissions:
        found_user = False
        permissions.append(filename)
        
        old = open('.permissions', 'r')
        new = open('.permissions.tmp', 'w+')

        for cur_account in old:
            permission_list = cur_account.split()
            if not permission_list:
                continue
            new.write(permission_list[0] + ' ')
            if permission_list[0] == account:
                found_user = True
                for add in permissions:
                    new.write(add + ' ')
            else:
                for permission in permission_list[1:]:
                    new.write(permission + ' ')
            new.write('\n')

        if not found_user:
            new.write(account + ' ' + filename + '\n')

        old.close()
        new.close()

        os.system('rm .permissions')
        os.system('mv .permissions.tmp .permissions')
