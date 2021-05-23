#!/usr/bin/python3

import socket
import base64
from datetime import datetime
import os
import secrets

IP = ''
PORT = 6969
MAXBYTES = 5 * 2**20 # 5 MB
PUBKEY_FILENAME = "pub.pem"
AES_KEY_LEN = 64

if __name__ == "__main__":
    # Instructions0
    print("Please ensure that this machine has an IP that agrees with the settings of the camera.")

    # Bind port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((IP, PORT))
        s.listen(1)
    except Exception as e:
        print(e)
        print("Error in binding port. Exiting...")
        exit()
    print("Port binding successful!")

    # Listen to port
    while True:
        print("Listening on port {}".format(PORT))
        # Accept connection and receive data
        (clientsocket, address) = s.accept()
        print("Incoming connection from {}".format(address))
        buff = clientsocket.recv(MAXBYTES)
        raw_data = bytearray()
        while buff:
            raw_data += buff
            buff = clientsocket.recv(MAXBYTES)
        print("Received {} bytes of data.".format(len(raw_data)))

        # Decode
        imgdata = base64.b64decode(raw_data)

        # Save plaintext data
        timestamp = datetime.now().strftime("%d-%b-%Y_%H-%M-%S")
        filename = "Data_{}".format(timestamp)
        with open(filename, "wb") as f:
            f.write(imgdata)
        
        # Generate AES key and save it to plaintext file
        aeskey = secrets.token_bytes(AES_KEY_LEN)
        with open("aeskey", "wb") as f:
            f.write(aeskey)
        # Encrypt AES key using RSA
        os.system("openssl rsautl -encrypt -inkey {} -pubin -in aeskey -out aeskey.sec".format(PUBKEY_FILENAME))

        # Encrypt data using the AES key
        os.system("openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -in {} -out {}.sec -pass stdin < aeskey".format(filename, filename))

        # Pack encrypted files into a tar
        os.system("tar -cf files.tar {}.sec aeskey.sec".format(filename))

        # Clean up
        os.system("rm {}*".format(filename))
        os.system("rm aeskey*")

