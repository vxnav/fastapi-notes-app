
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hash_password(password):
    return password_hasher.hash(password)

def verify_password(pass_received, pass_hash):
    return password_hasher.verify(pass_received, pass_hash)