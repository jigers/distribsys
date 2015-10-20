import socket
import sys
import random
import time
from reliable_socket import reliable_socket
HOST = "localhost"
PORT = 5005

rsock = reliable_socket()
msg = sys.stdin.readline().strip()
a = rsock.sendto(msg, (HOST, PORT))
if a:
	print "Successfully sent!"
else:
	print "Failed to send!"