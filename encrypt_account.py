import bcrypt

# encrypt string s
def encrypt(s):
    return bcrypt.hashpw(s.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# decrypt string s
def decrypt(s, hashed):
    return bcrypt.checkpw(s.encode('utf-8'), hashed.encode('utf-8'))
