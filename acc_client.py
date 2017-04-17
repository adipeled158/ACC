__author__ = 'user'
import socket

class Acc_client():
    def __init__(self, ip,port):
        self.ip = ip
        self.port = port
        self.socket = None
    def is_good_socket(self):
        """
        check if the server connect
        """
        try:
            self.socket = socket.socket()
            self.socket.connect((self.ip, self.port))
            print "After Connect"
            return True
        except:
            return False
    def send(self, data):
        """
        sending data to server

        """
        try:
            self.socket.send(data)
            return True
        except:
            return False

    def recv(self):
        """
        receiving data from server
        """
        try:
            data = self.socket.recv(10000)
            return data
        except:
            return None
