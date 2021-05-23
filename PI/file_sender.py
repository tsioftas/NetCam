#!/usr/bin/python3

import socket
import base64

TARGET_IP = ""
TARGET_PORT = 6969
FILENAME = "capture.jpg"

if __name__ == "__main__":
       # Read file data
       with open(FILENAME, "rb") as f:
              data = f.read()
       # Encode data using base64 encoding
       data = base64.encodebytes(data)
       # Send data to target
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
              s.connect((TARGET_IP, TARGET_PORT))
              s.send(data)
       


       