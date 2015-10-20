import socket
import sys
import random
import time
import os

class reliable_socket:
    timeout = 3
    HOST = ""
    PORT = ""
    def bind (self, (HOST, PORT)):
        self.PORT = PORT
        self.HOST = HOST
    def settimeout(self, timeout):
        self.timeout = timeout
    def gettimeout(self):
        return self.timeout
    def sendto(self, msg, (HOST, PORT)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	id = os.urandom(32)
	msg_bytes = bytearray(msg, "ascii")
	bytes ='0' + id + msg 
        sock.sendto(bytes, (HOST, PORT))
        send_time = time.clock()
        while (time.clock() - send_time < self.timeout):
            sock.settimeout(self.timeout - (time.clock()-send_time))
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                return False
            if (len(data) == 33 and data[0] == '1' and data[1:33] == id):
                sock.close()
                return True
        sock.close()
        return False
        
    def recvfrom(self, buffsize):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.HOST, self.PORT))
        data, addr = sock.recvfrom(buffsize)
        if (data[0] == '0'):
            ans = '1'+data[1:33]
            sock.sendto(ans, addr)
        sock.close()
        return (data[33:len(data)].decode("ascii"), addr)