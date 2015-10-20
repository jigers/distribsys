import socket
import sys
import random
import time
from reliable_socket import reliable_socket

HOST = "localhost"
PORT = 5005


rsock = reliable_socket()
rsock.bind((HOST, PORT))
print("listening on port %s" % PORT)
while True:
    data, addr = rsock.recvfrom(1024)
    print("received \"%s\" from %s" % (data, addr))