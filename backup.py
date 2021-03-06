from cryptography.fernet import Fernet
import os.path
import time
import ray

ray.init()

@ray.remote
def decrypt(path):

    key = open("key.key", "rb").read()
    f = Fernet(key)
    number_of_files = 0
    skipped = 0

    for dirpath, dirnames, files in os.walk(path):
        for file in files:

            number_of_files += 1
            loc = dirpath + "\\" + file
            with open(loc, 'rb') as data:
               
                encrypted_data = data.read()
                try:
                    # decrypt data
                    decrypted_data = f.decrypt(encrypted_data)
                except:
                    skipped += 1
                else:
                    # write the original file
                    with open(loc, "wb") as data:
                        data.write(decrypted_data)
    
    return (number_of_files, skipped)

#driver
if __name__ == "__main__":

    p = input('Provide the path of the drive:\n')
    print('Decrypting files...')
    start = time.time()
    result = decrypt.remote(p)
    result = ray.get(result)
    end = time.time()

    print(result[0] - result[1], 'files decrypted')
    # decrypted and skipped files
    if(result[1] > 0):
        print('skipped', result[1], 'files.\nfiles were either invalid or modified previously')
    print('time consumed =', end - start)
