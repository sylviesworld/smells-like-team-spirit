import bcrypt

def encrypt(s):
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(s.encode('utf8'), salt)
      
    return hashed.decode('utf8')

def decrypt(s, hashed):
    return bcrypt.checkpw(s.encode('utf8'), hashed.encode('utf8'))



