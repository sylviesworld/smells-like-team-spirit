# encrypt.py handles encryption and decryption of user/pass, email, and files with simple homophonic substitution cipher

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

# works exactly like get_encrypt but reads in the key/val pairs backward for decrypting
def get_decrypt():
    decrypt_pairs = dictionary()

    f = open('.encrypt', 'r')

    for line in f:
        pair = line.split()
        decrypt_pairs[pair[1]] = pair[0]

    f.close()

    return decrypt_pairs

# encrypts account email, builds new encrypted string from original string
def encrypt_email(raw_email):
    all_pairs = get_encrypt()

    # save the email "name" separate from the address to make cipher harder to brute force
    a = raw_email.find('@')
    email = raw_email[:a]
    address = raw_email[a:]

    encrypted_email = ''
    encrypted_address = ''

    for c in email:
        new_c = all_pairs[c]
        encrypted_email += new_c
    
    for c in address:
        new_c = all_pairs[c]
        encrypted_address += new_c

    encrypted_pair = [encrypted_email, encrypted_address]
    
    return encrypted_pair

# encrypts the given string
def encrypt(s):
    all_pairs = get_encrypt()

    encrypted_s = ''
    
    for c in s:
        new_c = all_pairs[c]
        encrypted_s += new_c

    return encrypted_s

# decrypts the given string
def decrypt(s):
    all_pairs = get_decrypt()

    decrypted_s = ''

    for c in s:
        new_c = all_pairs[c]
        decrypted_s += new_c

    return decrypted_s
