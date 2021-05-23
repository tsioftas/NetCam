#!/usr/bin/python3

import sys
import os

PRIVKEY_FILENAME = "key.pem"

if __name__ == "__main__":
    # First decrypt aeskey.sec to retrieve the AES key
    os.system("openssl rsautl -decrypt -inkey {} -in aeskey.sec -out aeskey.dec".format(PRIVKEY_FILENAME))

    # Read the AES key
    with open("aeskey.dec", "rb") as f:
        aeskey = f.read()
    
    # Decrypt the AES encrypted file
    filename = sys.argv[1]
    os.system("openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -d -in {} -out {}.dec -pass stdin < aeskey.dec".format(filename, filename))


    # Delete the plaintext aeskey file
    os.system("rm aeskey.dec")
    