from socket import * 

'''
class Server():
    def __init__(self, UDP_IP= "127.0.0.1", UDP_PORT= 5005) -> None:
        self.ip = UDP_IP
        self.port = UDP_PORT



    def run(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind((self.ip, self.port))
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            print("received message: %s" % data)
'''

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket(AF_INET, # Internet
                     SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    data.split() 