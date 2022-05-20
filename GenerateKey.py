from cryptography.fernet import Fernet
def gen_key():
    #Here will be Generating a key and save it
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

gen_key()
