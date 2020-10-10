# encrypt.py handles encryption of user/pass, email, and files with simple homophonic substitution cipher

# dictionary object contains key/val pairs
class dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value

# reads in encryption key from .encrypt and stores pairs in dictionary
# each letter and symbol corresponds to a random other character
def get_encrypt():
    encrypt_pairs = dictionary()

    f = open('.encrypt', 'r')

    for line in f:
        pair = line.split()
        encrypt_pairs[pair[0]] = pair[1]

    f.close()

    return encrypt_pairs

# encrypts account username and password, builds new encrypted string from original string
def encrypt_account(raw_user, raw_pass):
    all_pairs = get_encrypt()
    
    encrypted_user = ''
    encrypted_pass = ''

    # encrypt username
    for c in raw_user:
        new_c = all_pairs[c]
        encrypted_user += new_c
    
    # encrypt password
    for c in raw_pass:
        new_c = all_pairs[c]
        encrypted_pass += new_c

    # store encrypted user/pass pair in list that this function returns
    encrypted_pair = [encrypted_user, encrypted_pass]

    return encrypted_pair

# encrypts account email, builds new encrypted string from original string
def encrypt_email(raw_email):
    all_pairs = get_encrypt()

    # only worry about encrypting and saving part of email that comes before @, assume gmail
    raw_email = raw_email[:-10]

    encrypted_email = ''

    for c in raw_email:
        new_c = all_pairs[c]
        encrypted_email += new_c

    return encrypted_email
