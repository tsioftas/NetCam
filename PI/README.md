# Receiving and encrypting files

First time instructions:
1. ```chmod +x images_receiver.py```
2. Set static IP to 192.168.1.4

To receive and encrypt all you have to do is run ```./images_receiver.py```. Once data is received, this will produce an archive named _file.tar_ containing the encrypted data together with information for decrypting, which is in turn encrypted with the RSA public key contained in _pub.pem_. Therefore the encrypted file cannot be read without the corresponding private key.
